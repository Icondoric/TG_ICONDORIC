"""
PDF Report Service — Generación de informes formales de evaluación de candidatos.

Produce un documento A4 con:
  - Portada institucional
  - Resumen ejecutivo
  - Información de la convocatoria
  - Metodología de evaluación
  - Resultados y estadísticas
  - Ranking detallado de candidatos
  - Anexos: CV en formato Harvard por cada candidato
"""

import logging
import random
import string
from datetime import datetime
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────
#  Paleta de colores corporativos
# ─────────────────────────────────────────
NAVY       = colors.HexColor('#1B3A6B')
NAVY_MED   = colors.HexColor('#2C5282')
NAVY_LIGHT = colors.HexColor('#EBF8FF')
GOLD       = colors.HexColor('#B7791F')
GOLD_LIGHT = colors.HexColor('#FEFCBF')
GRAY_LIGHT = colors.HexColor('#F7FAFC')
GRAY_MED   = colors.HexColor('#E2E8F0')
GRAY_DARK  = colors.HexColor('#4A5568')
WHITE      = colors.white
BLACK      = colors.black

APTO_BG    = colors.HexColor('#F0FFF4')
APTO_FG    = colors.HexColor('#276749')
CONSID_BG  = colors.HexColor('#EBF8FF')
CONSID_FG  = colors.HexColor('#2C5282')
NOAPTO_BG  = colors.HexColor('#FFF5F5')
NOAPTO_FG  = colors.HexColor('#C53030')

ANNEX_LETTERS = [chr(i) for i in range(ord('A'), ord('Z') + 1)]

_MESES_ES = [
    '', 'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
    'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre',
]


def _date_es(dt: datetime) -> str:
    return f'{dt.day} de {_MESES_ES[dt.month]} de {dt.year}'


class PDFReportService:
    """
    Genera informes ejecutivos de evaluación de candidatos en formato PDF.
    Utiliza ReportLab con diseño Harvard para los CVs y estilo institucional
    para el cuerpo del informe.
    """

    PAGE_W, PAGE_H = A4

    def __init__(self):
        self.styles = self._build_styles()

    # ─────────────────────────────────────────
    #  Estilos tipográficos
    # ─────────────────────────────────────────
    def _build_styles(self) -> dict:
        return {
            # Portada
            'cover_system': ParagraphStyle(
                'cover_system', fontName='Helvetica', fontSize=9,
                textColor=GRAY_DARK, alignment=TA_CENTER, spaceAfter=4,
            ),
            'cover_title': ParagraphStyle(
                'cover_title', fontName='Helvetica-Bold', fontSize=22,
                textColor=NAVY, alignment=TA_CENTER, spaceAfter=8, leading=28,
            ),
            'cover_subtitle': ParagraphStyle(
                'cover_subtitle', fontName='Helvetica-Bold', fontSize=14,
                textColor=NAVY_MED, alignment=TA_CENTER, spaceAfter=4, leading=18,
            ),
            'cover_institution': ParagraphStyle(
                'cover_institution', fontName='Helvetica', fontSize=12,
                textColor=GRAY_DARK, alignment=TA_CENTER, spaceAfter=24,
            ),
            'cover_meta': ParagraphStyle(
                'cover_meta', fontName='Helvetica', fontSize=9,
                textColor=GRAY_DARK, alignment=TA_LEFT,
            ),
            'confidential': ParagraphStyle(
                'confidential', fontName='Helvetica-Bold', fontSize=8,
                textColor=colors.HexColor('#C53030'), alignment=TA_CENTER,
            ),
            # Cuerpo
            'section_title': ParagraphStyle(
                'section_title', fontName='Helvetica-Bold', fontSize=13,
                textColor=NAVY, spaceBefore=18, spaceAfter=6,
            ),
            'subsection_title': ParagraphStyle(
                'subsection_title', fontName='Helvetica-Bold', fontSize=10,
                textColor=NAVY_MED, spaceBefore=12, spaceAfter=4,
            ),
            'candidate_header': ParagraphStyle(
                'candidate_header', fontName='Helvetica-Bold', fontSize=11,
                textColor=NAVY, spaceBefore=14, spaceAfter=4,
            ),
            'body': ParagraphStyle(
                'body', fontName='Helvetica', fontSize=9.5, textColor=BLACK,
                leading=14, spaceAfter=6, alignment=TA_JUSTIFY,
            ),
            'body_sm': ParagraphStyle(
                'body_sm', fontName='Helvetica', fontSize=8.5,
                textColor=GRAY_DARK, leading=12, spaceAfter=4,
            ),
            'label': ParagraphStyle(
                'label', fontName='Helvetica-Bold', fontSize=8.5, textColor=GRAY_DARK,
            ),
            'cell': ParagraphStyle(
                'cell', fontName='Helvetica', fontSize=8.5, textColor=BLACK, leading=12,
            ),
            'cell_bold': ParagraphStyle(
                'cell_bold', fontName='Helvetica-Bold', fontSize=8.5, textColor=BLACK, leading=12,
            ),
            'cell_header': ParagraphStyle(
                'cell_header', fontName='Helvetica-Bold', fontSize=8.5,
                textColor=WHITE, leading=12,
            ),
            # Harvard CV
            'cv_name': ParagraphStyle(
                'cv_name', fontName='Helvetica-Bold', fontSize=18,
                textColor=NAVY, alignment=TA_CENTER, spaceAfter=4,
            ),
            'cv_contact': ParagraphStyle(
                'cv_contact', fontName='Helvetica', fontSize=9,
                textColor=GRAY_DARK, alignment=TA_CENTER, spaceAfter=8,
            ),
            'cv_section': ParagraphStyle(
                'cv_section', fontName='Helvetica-Bold', fontSize=10,
                textColor=NAVY, spaceBefore=12, spaceAfter=2,
            ),
            'cv_entry_title': ParagraphStyle(
                'cv_entry_title', fontName='Helvetica-Bold', fontSize=9.5,
                textColor=BLACK, spaceAfter=1,
            ),
            'cv_entry_subtitle': ParagraphStyle(
                'cv_entry_subtitle', fontName='Helvetica-Oblique', fontSize=9,
                textColor=GRAY_DARK, spaceAfter=2,
            ),
            'cv_bullet': ParagraphStyle(
                'cv_bullet', fontName='Helvetica', fontSize=9, textColor=BLACK,
                leftIndent=12, spaceAfter=1, leading=12,
            ),
            'cv_skills': ParagraphStyle(
                'cv_skills', fontName='Helvetica', fontSize=9,
                textColor=BLACK, leading=14, spaceAfter=4,
            ),
        }

    # ─────────────────────────────────────────
    #  Utilidades
    # ─────────────────────────────────────────
    @staticmethod
    def _gen_ref() -> str:
        year = datetime.now().year
        suffix = ''.join(random.choices(string.digits, k=6))
        return f'EVA-{year}-{suffix}'

    @staticmethod
    def _fmt_date(d: str) -> str:
        if not d:
            return '—'
        try:
            return datetime.fromisoformat(d[:10]).strftime('%d/%m/%Y')
        except Exception:
            return str(d)

    @staticmethod
    def _clsf_colors(clasificacion: str):
        if clasificacion == 'APTO':
            return APTO_BG, APTO_FG
        if clasificacion == 'CONSIDERADO':
            return CONSID_BG, CONSID_FG
        return NOAPTO_BG, NOAPTO_FG

    # ─────────────────────────────────────────
    #  Callbacks header/footer
    # ─────────────────────────────────────────
    def _make_callbacks(self, ref: str, offer_title: str):
        pw, ph = self.PAGE_W, self.PAGE_H
        short_title = offer_title[:50] + ('…' if len(offer_title) > 50 else '')

        def _first_page(canvas, doc):
            pass  # Sin header/footer en portada

        def _later_pages(canvas, doc):
            canvas.saveState()
            # Línea superior
            canvas.setStrokeColor(NAVY)
            canvas.setLineWidth(0.4)
            canvas.line(2.5 * cm, ph - 1.8 * cm, pw - 2.5 * cm, ph - 1.8 * cm)
            # Header izquierda
            canvas.setFont('Helvetica', 7.5)
            canvas.setFillColor(NAVY_MED)
            canvas.drawString(2.5 * cm, ph - 1.55 * cm,
                              'Sistema de Evaluación de Perfiles Profesionales — EMI')
            # Header derecha (CONFIDENCIAL)
            canvas.setFont('Helvetica-Bold', 7.5)
            canvas.setFillColor(colors.HexColor('#C53030'))
            canvas.drawRightString(pw - 2.5 * cm, ph - 1.55 * cm, 'CONFIDENCIAL')
            # Línea inferior
            canvas.setStrokeColor(GRAY_MED)
            canvas.setLineWidth(0.4)
            canvas.line(2.5 * cm, 1.8 * cm, pw - 2.5 * cm, 1.8 * cm)
            # Footer izquierda: referencia
            canvas.setFont('Helvetica', 7)
            canvas.setFillColor(GRAY_DARK)
            canvas.drawString(2.5 * cm, 1.3 * cm, ref)
            # Footer centro: número de página
            canvas.drawCentredString(pw / 2, 1.3 * cm, f'Página {doc.page}')
            # Footer derecha: título oferta
            canvas.drawRightString(pw - 2.5 * cm, 1.3 * cm, short_title)
            canvas.restoreState()

        return _first_page, _later_pages

    # ─────────────────────────────────────────
    #  Flowable helpers
    # ─────────────────────────────────────────
    def _hr(self, color=GRAY_MED, thickness=0.5):
        return HRFlowable(width='100%', thickness=thickness, color=color, spaceAfter=6, spaceBefore=4)

    def _hr_navy(self):
        return HRFlowable(width='100%', thickness=1, color=NAVY, spaceAfter=6, spaceBefore=2)

    def _spacer(self, h=6):
        return Spacer(1, h)

    def _p(self, text, style='body'):
        return Paragraph(str(text), self.styles[style])

    def _section_header(self, text: str) -> list:
        return [self._p(text, 'section_title'), self._hr_navy()]

    def _subsection(self, text: str) -> list:
        return [self._p(text, 'subsection_title'), self._hr(thickness=0.3)]

    def _info_table(self, rows: list) -> Table:
        """Tabla de dos columnas: etiqueta → valor."""
        data = [
            [Paragraph(label, self.styles['label']),
             Paragraph(str(value) if value else '—', self.styles['cell'])]
            for label, value in rows
        ]
        t = Table(data, colWidths=[4.5 * cm, None])
        t.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('LINEBELOW', (0, 0), (-1, -2), 0.2, GRAY_MED),
        ]))
        return t

    def _stats_table(self, header: list, rows: list) -> Table:
        """Tabla con encabezado navy y filas alternas."""
        header_cells = [Paragraph(h, self.styles['cell_header']) for h in header]
        data = [header_cells] + [
            [Paragraph(str(c), self.styles['cell']) for c in row]
            for row in rows
        ]
        col_w = (self.PAGE_W - 5 * cm) / len(header)
        t = Table(data, colWidths=[col_w] * len(header), repeatRows=1)
        style = [
            ('BACKGROUND', (0, 0), (-1, 0), NAVY),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, 0), 7),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 7),
            ('TOPPADDING', (0, 1), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
            ('GRID', (0, 0), (-1, -1), 0.3, GRAY_MED),
        ]
        for i in range(1, len(rows) + 1):
            if i % 2 == 0:
                style.append(('BACKGROUND', (0, i), (-1, i), GRAY_LIGHT))
        t.setStyle(TableStyle(style))
        return t

    # ─────────────────────────────────────────
    #  PORTADA
    # ─────────────────────────────────────────
    def _build_cover(self, oferta: dict, ref: str) -> list:
        institution = oferta.get('institution_name') or 'Institución'
        titulo = oferta.get('titulo', 'Convocatoria')
        tipo_label = 'Pasantía' if oferta.get('tipo') == 'pasantia' else 'Empleo'
        date_str = _date_es(datetime.now())

        story = [Spacer(1, 5 * cm)]

        story.append(self._p('SISTEMA DE EVALUACIÓN DE PERFILES PROFESIONALES', 'cover_system'))
        story.append(self._p('Escuela Militar de Ingeniería — EMI', 'cover_system'))
        story.append(Spacer(1, 0.4 * cm))
        story.append(HRFlowable(width='60%', thickness=1.5, color=GOLD,
                                spaceAfter=10, spaceBefore=0, hAlign='CENTER'))
        story.append(self._p('INFORME DE EVALUACIÓN DE CANDIDATOS', 'cover_title'))
        story.append(HRFlowable(width='60%', thickness=0.5, color=NAVY_MED,
                                spaceAfter=14, spaceBefore=0, hAlign='CENTER'))
        story.append(self._p(titulo, 'cover_subtitle'))
        story.append(self._p(institution, 'cover_institution'))

        # Tabla de metadatos centrada
        meta_rows = [
            ('Convocatoria', titulo),
            ('Institución', institution),
            ('Tipo', tipo_label),
        ]
        if oferta.get('area'):
            meta_rows.append(('Área', oferta['area']))
        meta_rows += [
            ('Fecha de emisión', date_str),
            ('Número de referencia', ref),
        ]

        meta_data = [
            [Paragraph(k, self.styles['label']), Paragraph(v, self.styles['cover_meta'])]
            for k, v in meta_rows
        ]
        meta_t = Table(meta_data, colWidths=[4.5 * cm, 9 * cm], hAlign='CENTER')
        meta_t.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LINEBELOW', (0, 0), (-1, -2), 0.3, GRAY_MED),
        ]))
        story.append(meta_t)
        story.append(Spacer(1, 3 * cm))

        # Aviso de confidencialidad
        story.append(self._hr())
        story.append(self._p(
            'DOCUMENTO CONFIDENCIAL — El presente informe contiene información reservada sobre '
            'candidatos evaluados. Su distribución está restringida al personal autorizado '
            'de la institución destinataria.',
            'confidential',
        ))
        story.append(self._hr())
        story.append(PageBreak())
        return story

    # ─────────────────────────────────────────
    #  1. RESUMEN EJECUTIVO
    # ─────────────────────────────────────────
    def _build_summary(self, oferta: dict, candidatos: list,
                       total_postulantes: int, top_n: int,
                       annex_refs: list) -> list:
        story = []
        story += self._section_header('1. RESUMEN EJECUTIVO')

        apto       = sum(1 for c in candidatos if c.get('clasificacion') == 'APTO')
        considerado = sum(1 for c in candidatos if c.get('clasificacion') == 'CONSIDERADO')
        no_apto    = sum(1 for c in candidatos if c.get('clasificacion') == 'NO_APTO')
        best       = candidatos[0] if candidatos else None
        best_score = round(best['match_score'] * 100) if best else 0
        best_name  = best['perfil']['nombre_completo'] if best else '—'
        institution = oferta.get('institution_name') or 'la institución solicitante'

        scores_top = [c['match_score'] for c in candidatos if c.get('match_score') is not None]
        avg_top = round(sum(scores_top) / len(scores_top) * 100) if scores_top else 0

        story.append(self._p(
            f'El presente informe sintetiza los resultados del proceso de evaluación de candidatos '
            f'para la convocatoria <b>"{oferta.get("titulo", "")}"</b> publicada por '
            f'<b>{institution}</b>. El sistema de evaluación automatizado procesó un total de '
            f'<b>{total_postulantes} postulación{"es" if total_postulantes != 1 else ""}</b>, '
            f'de las cuales se presentan los <b>{len(candidatos)} candidatos</b> con mayor '
            f'correspondencia al perfil requerido, ordenados de forma descendente según su '
            f'puntaje de compatibilidad global.',
            'body',
        ))

        story.append(self._spacer(8))
        story.append(self._stats_table(
            ['Total postulantes', 'APTO', 'CONSIDERADO', 'NO APTO', 'Mejor puntaje', 'Promedio top'],
            [[str(total_postulantes), str(apto), str(considerado),
              str(no_apto), f'{best_score}%', f'{avg_top}%']],
        ))
        story.append(self._spacer(8))

        if best and annex_refs:
            if len(annex_refs) > 1:
                refs_str = ', '.join(annex_refs[:-1]) + f' y {annex_refs[-1]}'
            else:
                refs_str = annex_refs[0]
            story.append(self._p(
                f'El candidato con mayor puntaje de correspondencia es <b>{best_name}</b>, '
                f'quien obtuvo un índice de <b>{best_score}%</b>, clasificado como '
                f'<b>{best.get("clasificacion", "—")}</b>. Los perfiles profesionales completos '
                f'de los candidatos seleccionados se incluyen como {refs_str} al final del '
                f'presente documento.',
                'body',
            ))

        story.append(PageBreak())
        return story

    # ─────────────────────────────────────────
    #  2. INFORMACIÓN DE LA CONVOCATORIA
    # ─────────────────────────────────────────
    def _build_oferta_info(self, oferta: dict) -> list:
        story = []
        story += self._section_header('2. INFORMACIÓN DE LA CONVOCATORIA')
        story.append(self._p(
            'En esta sección se detallan todas las características de la convocatoria laboral '
            'para la cual se realizó el proceso de evaluación, incluyendo las condiciones de '
            'la oferta, el objetivo de la convocatoria y el perfil de candidato requerido.',
            'body',
        ))
        story.append(self._spacer(6))

        story += self._subsection('2.1 Datos generales')
        tipo_label = 'Pasantía' if oferta.get('tipo') == 'pasantia' else 'Empleo'
        general_rows = [
            ('Título', oferta.get('titulo', '—')),
            ('Institución', oferta.get('institution_name') or '—'),
            ('Sector', oferta.get('sector') or '—'),
            ('Tipo', tipo_label),
            ('Modalidad', (oferta.get('modalidad') or '—').capitalize()),
            ('Área', oferta.get('area') or '—'),
            ('Ubicación', oferta.get('ubicacion') or '—'),
            ('Cupos disponibles', str(oferta.get('cupos_disponibles') or '—')),
            ('Fecha inicio', self._fmt_date(oferta.get('fecha_inicio'))),
            ('Fecha cierre', self._fmt_date(oferta.get('fecha_cierre'))),
            ('Estado', 'Activa' if oferta.get('is_active') else 'Cerrada'),
        ]
        if oferta.get('contact_email'):
            general_rows.append(('Correo de contacto', oferta['contact_email']))
        if oferta.get('contact_phone'):
            general_rows.append(('Teléfono de contacto', oferta['contact_phone']))
        story.append(self._info_table(general_rows))
        story.append(self._spacer(8))

        if oferta.get('descripcion'):
            story += self._subsection('2.2 Objetivo de la convocatoria')
            story.append(self._p(oferta['descripcion'], 'body'))
            story.append(self._spacer(6))

        req = oferta.get('requirements') or {}
        has_req = (
            req.get('required_education_level') or
            req.get('min_experience_years', 0) > 0 or
            req.get('required_skills') or
            req.get('preferred_skills') or
            req.get('required_languages')
        )
        if has_req:
            story += self._subsection('2.3 Perfil requerido')
            req_rows = []
            if req.get('required_education_level'):
                req_rows.append(('Nivel educativo mínimo', req['required_education_level']))
            if req.get('min_experience_years', 0) > 0:
                req_rows.append(('Experiencia mínima', f"{req['min_experience_years']} año(s)"))
            if req.get('required_skills'):
                req_rows.append(('Habilidades requeridas', ', '.join(req['required_skills'])))
            if req.get('preferred_skills'):
                req_rows.append(('Habilidades deseables', ', '.join(req['preferred_skills'])))
            if req.get('required_languages'):
                req_rows.append(('Idiomas requeridos', ', '.join(req['required_languages'])))
            story.append(self._info_table(req_rows))

        story.append(PageBreak())
        return story

    # ─────────────────────────────────────────
    #  3. METODOLOGÍA
    # ─────────────────────────────────────────
    def _build_methodology(self, oferta: dict) -> list:
        story = []
        story += self._section_header('3. METODOLOGÍA DE EVALUACIÓN')
        story.append(self._p(
            'La evaluación de candidatos se realiza mediante un modelo de correspondencia '
            'multidimensional basado en Regresión Ridge (Ridge Regression). El modelo compara el perfil '
            'del candidato con los requisitos específicos de la convocatoria a lo largo de '
            'cinco dimensiones ponderadas, produciendo un puntaje de compatibilidad global '
            'comprendido entre 0% y 100%.',
            'body',
        ))
        story.append(self._spacer(8))

        story += self._subsection('3.1 Dimensiones de evaluación y ponderación')
        weights = oferta.get('weights') or {}
        dim_rows = [
            ['Dimensión', 'Descripción', 'Peso'],
            ['Habilidades técnicas',
             'Correspondencia entre las habilidades técnicas del candidato y las requeridas por la oferta',
             f"{round(weights.get('hard_skills_weight', 0.35) * 100)}%"],
            ['Habilidades blandas',
             'Alineación de competencias interpersonales y de gestión con el perfil solicitado',
             f"{round(weights.get('soft_skills_weight', 0.20) * 100)}%"],
            ['Formación académica',
             'Adecuación del nivel educativo y área de estudio al perfil requerido',
             f"{round(weights.get('education_weight', 0.20) * 100)}%"],
            ['Experiencia profesional',
             'Correspondencia de los años de experiencia laboral acreditada',
             f"{round(weights.get('experience_weight', 0.15) * 100)}%"],
            ['Idiomas',
             'Coincidencia con los idiomas requeridos por la convocatoria',
             f"{round(weights.get('languages_weight', 0.10) * 100)}%"],
        ]
        header_row = [Paragraph(h, self.styles['cell_header']) for h in dim_rows[0]]
        data = [header_row] + [
            [Paragraph(c, self.styles['cell']) for c in row] for row in dim_rows[1:]
        ]
        pw = self.PAGE_W - 5 * cm
        dim_t = Table(data, colWidths=[3.5 * cm, pw - 5.5 * cm, 2 * cm], repeatRows=1)
        dim_t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), NAVY),
            ('ALIGN', (2, 0), (2, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('GRID', (0, 0), (-1, -1), 0.3, GRAY_MED),
            ('BACKGROUND', (0, 2), (-1, 2), GRAY_LIGHT),
            ('BACKGROUND', (0, 4), (-1, 4), GRAY_LIGHT),
        ]))
        story.append(dim_t)
        story.append(self._spacer(10))

        story += self._subsection('3.2 Umbrales de clasificación')
        thresholds = oferta.get('thresholds') or {}
        apto_th   = round(thresholds.get('apto_threshold', 0.70) * 100)
        consid_th = round(thresholds.get('considerado_threshold', 0.50) * 100)

        thr_rows = [
            ['Clasificación', 'Rango de puntaje', 'Interpretación'],
            ['APTO',        f'≥ {apto_th}%',
             'El candidato cumple satisfactoriamente con el perfil requerido'],
            ['CONSIDERADO', f'{consid_th}%–{apto_th - 1}%',
             'El candidato cumple parcialmente; puede ser evaluado con reservas'],
            ['NO APTO',     f'< {consid_th}%',
             'El candidato no alcanza el umbral mínimo de correspondencia'],
        ]
        clsf_bgs = [None, APTO_BG, CONSID_BG, NOAPTO_BG]
        clsf_fgs = [None, APTO_FG, CONSID_FG, NOAPTO_FG]
        header2 = [Paragraph(h, self.styles['cell_header']) for h in thr_rows[0]]
        data2 = [header2] + [
            [Paragraph(c, self.styles['cell']) for c in row] for row in thr_rows[1:]
        ]
        thr_t = Table(data2, colWidths=[2.8 * cm, 3 * cm, pw - 5.8 * cm], repeatRows=1)
        thr_style = [
            ('BACKGROUND', (0, 0), (-1, 0), NAVY),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('GRID', (0, 0), (-1, -1), 0.3, GRAY_MED),
        ]
        for i in range(1, 4):
            thr_style += [
                ('BACKGROUND', (0, i), (-1, i), clsf_bgs[i]),
                ('TEXTCOLOR', (0, i), (-1, i), clsf_fgs[i]),
                ('FONTNAME', (0, i), (0, i), 'Helvetica-Bold'),
            ]
        thr_t.setStyle(TableStyle(thr_style))
        story.append(thr_t)
        story.append(PageBreak())
        return story

    # ─────────────────────────────────────────
    #  4. RESULTADOS Y ESTADÍSTICAS
    # ─────────────────────────────────────────
    def _build_statistics(self, candidatos: list, total_postulantes: int,
                          annex_refs: list) -> list:
        story = []
        story += self._section_header('4. RESULTADOS Y ESTADÍSTICAS')
        story.append(self._p(
            'En esta sección se presenta la distribución de candidatos por clasificación '
            'y la tabla de puntajes individuales de los candidatos preseleccionados que '
            'conforman el ranking final de recomendación.',
            'body',
        ))
        story.append(self._spacer(8))

        story += self._subsection('4.1 Distribución por clasificación — candidatos del ranking')
        apto       = sum(1 for c in candidatos if c.get('clasificacion') == 'APTO')
        considerado = sum(1 for c in candidatos if c.get('clasificacion') == 'CONSIDERADO')
        no_apto    = sum(1 for c in candidatos if c.get('clasificacion') == 'NO_APTO')
        total_top  = len(candidatos) or 1
        story.append(self._stats_table(
            ['Clasificación', 'Cantidad', 'Porcentaje'],
            [
                ['APTO',       str(apto),       f'{round(apto / total_top * 100)}%'],
                ['CONSIDERADO', str(considerado), f'{round(considerado / total_top * 100)}%'],
                ['NO APTO',    str(no_apto),    f'{round(no_apto / total_top * 100)}%'],
            ],
        ))
        story.append(self._spacer(10))

        story += self._subsection('4.2 Puntajes individuales — candidatos seleccionados')
        pw = self.PAGE_W - 5 * cm
        scores_header = [Paragraph(h, self.styles['cell_header'])
                         for h in ['#', 'Candidato', 'Puntaje', 'Clasificación', 'Referencia']]
        scores_data = [scores_header]
        scores_style = [
            ('BACKGROUND', (0, 0), (-1, 0), NAVY),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('GRID', (0, 0), (-1, -1), 0.3, GRAY_MED),
        ]
        for i, c in enumerate(candidatos, start=1):
            annex = annex_refs[c['rank'] - 1] if c['rank'] - 1 < len(annex_refs) else '—'
            bg, _ = self._clsf_colors(c.get('clasificacion', ''))
            scores_data.append([
                Paragraph(f"#{c['rank']}", self.styles['cell']),
                Paragraph(c['perfil']['nombre_completo'], self.styles['cell']),
                Paragraph(f"{round(c['match_score'] * 100)}%", self.styles['cell_bold']),
                Paragraph(c.get('clasificacion', '—'), self.styles['cell']),
                Paragraph(annex, self.styles['cell']),
            ])
            scores_style.append(('BACKGROUND', (0, i), (-1, i), bg))

        score_t = Table(scores_data,
                        colWidths=[1.2 * cm, pw - 9 * cm, 2.5 * cm, 3 * cm, 2.3 * cm],
                        repeatRows=1)
        score_t.setStyle(TableStyle(scores_style))
        story.append(score_t)
        story.append(PageBreak())
        return story

    # ─────────────────────────────────────────
    #  5. RANKING DE CANDIDATOS
    # ─────────────────────────────────────────
    def _build_ranking(self, candidatos: list, annex_refs: list) -> list:
        story = []
        story += self._section_header('5. RANKING DE CANDIDATOS RECOMENDADOS')
        story.append(self._p(
            'A continuación se presenta la evaluación individual de cada candidato '
            'seleccionado, incluyendo el desglose de puntajes por dimensión, las fortalezas '
            'y áreas de mejora identificadas por el modelo, y una referencia al Currículo '
            'Vitae completo incluido en los anexos.',
            'body',
        ))
        story.append(self._spacer(10))

        DIM_LABELS = {
            'hard_skills_score':  'Habilidades Técnicas',
            'soft_skills_score':  'Habilidades Blandas',
            'education_score':    'Formación Académica',
            'experience_score':   'Experiencia Profesional',
            'languages_score':    'Idiomas',
        }
        pw = self.PAGE_W - 5 * cm

        for c in candidatos:
            annex   = annex_refs[c['rank'] - 1] if c['rank'] - 1 < len(annex_refs) else '—'
            nombre  = c['perfil']['nombre_completo']
            clsf    = c.get('clasificacion', 'NO_APTO')
            score   = round(c['match_score'] * 100)
            bg, fg  = self._clsf_colors(clsf)
            perfil  = c['perfil']

            block = []

            # Sub-encabezado
            block.append(self._p(
                f'5.{c["rank"]}  Candidato #{c["rank"]}: {nombre} &nbsp;— {annex}',
                'candidate_header',
            ))
            block.append(self._hr(thickness=0.5))

            # Score box + datos básicos
            info_parts = []
            if perfil.get('email'):
                info_parts.append(f'<b>Correo:</b> {perfil["email"]}')
            if perfil.get('telefono'):
                info_parts.append(f'<b>Teléfono:</b> {perfil["telefono"]}')
            if perfil.get('education_level'):
                info_parts.append(f'<b>Formación:</b> {perfil["education_level"]}')
            if perfil.get('experience_years', 0) > 0:
                info_parts.append(f'<b>Experiencia:</b> {perfil["experience_years"]} año(s)')
            if perfil.get('languages'):
                langs = perfil['languages'] if isinstance(perfil['languages'], list) else [str(perfil['languages'])]
                info_parts.append(f'<b>Idiomas:</b> {", ".join(langs)}')

            score_box = Paragraph(
                f'<font size="20"><b>{score}%</b></font><br/>'
                f'<font size="8">{clsf}</font>',
                ParagraphStyle('sbox', fontName='Helvetica-Bold',
                               alignment=TA_CENTER, textColor=fg, leading=22),
            )
            info_para = Paragraph('<br/>'.join(info_parts), self.styles['body_sm'])

            hdr_t = Table([[score_box, info_para]], colWidths=[3 * cm, None])
            hdr_t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, 0), bg),
                ('BOX', (0, 0), (0, 0), 0.5, fg),
                ('BOX', (1, 0), (1, 0), 0.3, GRAY_MED),
                ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ]))
            block.append(hdr_t)
            block.append(self._spacer(8))

            # Scores por dimensión
            scores_det = c.get('scores_detalle') or {}
            dim_rows_data = []
            for key, label in DIM_LABELS.items():
                val = scores_det.get(key)
                if val is None:
                    continue
                pct = round(val * 100)
                if pct >= 70:
                    estado, rbg, rfg = 'APTO',   APTO_BG,   APTO_FG
                elif pct >= 50:
                    estado, rbg, rfg = 'CONSID.', CONSID_BG, CONSID_FG
                else:
                    estado, rbg, rfg = 'BAJO',   NOAPTO_BG, NOAPTO_FG
                dim_rows_data.append((label, f'{pct}%', estado, rbg, rfg))

            if dim_rows_data:
                dim_header = [Paragraph(h, self.styles['cell_header'])
                              for h in ['Dimensión', 'Puntaje', 'Estado']]
                dim_data = [dim_header]
                dim_style = [
                    ('BACKGROUND', (0, 0), (-1, 0), NAVY),
                    ('TOPPADDING', (0, 0), (-1, -1), 4),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                    ('GRID', (0, 0), (-1, -1), 0.3, GRAY_MED),
                    ('ALIGN', (1, 0), (2, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ]
                for i, (lbl, pct_str, estado, rbg, rfg) in enumerate(dim_rows_data, 1):
                    dim_data.append([
                        Paragraph(lbl, self.styles['cell']),
                        Paragraph(pct_str, ParagraphStyle(
                            f'dpct{i}', fontName='Helvetica-Bold',
                            fontSize=8.5, textColor=rfg, alignment=TA_CENTER)),
                        Paragraph(estado, ParagraphStyle(
                            f'dest{i}', fontName='Helvetica-Bold',
                            fontSize=8, textColor=rfg, alignment=TA_CENTER)),
                    ])
                    dim_style += [
                        ('BACKGROUND', (0, i), (-1, i), rbg),
                        ('TEXTCOLOR', (0, i), (-1, i), rfg),
                    ]
                dim_t = Table(dim_data, colWidths=[pw - 4.5 * cm, 2 * cm, 2.5 * cm], repeatRows=1)
                dim_t.setStyle(TableStyle(dim_style))
                block.append(self._p('Desglose de puntajes por dimensión evaluada:', 'label'))
                block.append(self._spacer(3))
                block.append(dim_t)
                block.append(self._spacer(8))

            # Fortalezas y debilidades
            fortalezas = c.get('fortalezas') or []
            debilidades = c.get('debilidades') or []
            if fortalezas or debilidades:
                fd_data = []
                if fortalezas:
                    fd_data.append([
                        Paragraph('Fortalezas identificadas', self.styles['label']),
                        Paragraph(', '.join(fortalezas), self.styles['cell']),
                    ])
                if debilidades:
                    fd_data.append([
                        Paragraph('Áreas de mejora', self.styles['label']),
                        Paragraph(', '.join(debilidades), self.styles['cell']),
                    ])
                fd_t = Table(fd_data, colWidths=[4 * cm, None])
                fd_t.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('TOPPADDING', (0, 0), (-1, -1), 4),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                    ('LINEBELOW', (0, 0), (-1, -2), 0.2, GRAY_MED),
                ]))
                block.append(fd_t)
                block.append(self._spacer(6))

            # Referencia al anexo
            block.append(self._p(
                f'El Currículum completo de este candidato se encuentra en el '
                f'<b>{annex}</b> del presente documento.',
                'body_sm',
            ))
            block.append(self._hr(thickness=0.3))

            # Mantener encabezado + score box juntos; el resto fluye
            if len(block) >= 4:
                story.append(KeepTogether(block[:4]))
                story.extend(block[4:])
            else:
                story.extend(block)
            story.append(self._spacer(4))

        story.append(PageBreak())
        return story

    # ─────────────────────────────────────────
    #  ANEXOS — Harvard CV
    # ─────────────────────────────────────────
    def _build_cv_annex(self, candidato: dict, annex_letter: str) -> list:
        story = []
        story.append(self._p(f'ANEXO {annex_letter} — CURRICULUM ', 'section_title'))
        story.append(self._hr_navy())

        perfil  = candidato.get('perfil', {})
        gemini  = candidato.get('gemini_extraction') or {}
        personal = gemini.get('personal_info') or {}

        nombre    = perfil.get('nombre_completo') or 'Nombre no disponible'
        email     = perfil.get('email') or ''
        telefono  = perfil.get('telefono') or ''
        direccion = perfil.get('direccion') or personal.get('address') or ''

        # ── Nombre ──
        story.append(Spacer(1, 0.3 * cm))
        story.append(self._p(nombre.upper(), 'cv_name'))

        contact_parts = [p for p in [email, telefono, direccion] if p]
        if contact_parts:
            story.append(self._p(' &nbsp;|&nbsp; '.join(contact_parts), 'cv_contact'))

        story.append(HRFlowable(width='100%', thickness=1.5, color=NAVY,
                                spaceAfter=10, spaceBefore=4))

        # ── Perfil profesional ──
        summary = personal.get('summary') or perfil.get('summary') or ''
        if summary:
            story.append(self._p('PERFIL PROFESIONAL', 'cv_section'))
            story.append(self._hr(thickness=0.4))
            story.append(self._p(str(summary), 'body'))
            story.append(self._spacer(4))

        # ── Formación académica ──
        education = gemini.get('education') or []
        if education:
            story.append(self._p('FORMACIÓN ACADÉMICA', 'cv_section'))
            story.append(self._hr(thickness=0.4))
            for edu in sorted(education, key=lambda e: str(e.get('year', '0')), reverse=True):
                degree      = edu.get('degree') or edu.get('title') or '—'
                institution = edu.get('institution') or '—'
                year        = str(edu.get('year') or '—')
                field       = edu.get('field') or edu.get('area') or ''
                label_str   = f'<b>{degree}</b>' + (f' — {field}' if field else '')

                edu_row = [[
                    Paragraph(label_str, self.styles['cv_entry_title']),
                    Paragraph(year, ParagraphStyle(
                        'yr', fontName='Helvetica', fontSize=9,
                        textColor=GRAY_DARK, alignment=TA_RIGHT)),
                ]]
                edu_t = Table(edu_row, colWidths=[None, 2 * cm])
                edu_t.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
                    ('TOPPADDING', (0, 0), (-1, -1), 2),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
                ]))
                story.append(edu_t)
                story.append(self._p(institution, 'cv_entry_subtitle'))
            story.append(self._spacer(4))

        # ── Experiencia profesional ──
        experience = gemini.get('experience') or []
        if experience:
            story.append(self._p('EXPERIENCIA PROFESIONAL', 'cv_section'))
            story.append(self._hr(thickness=0.4))
            for exp in experience:
                role        = exp.get('role') or exp.get('position') or exp.get('title') or '—'
                company     = exp.get('company') or exp.get('organization') or '—'
                duration    = exp.get('duration') or exp.get('period') or ''
                description = exp.get('description') or exp.get('responsibilities') or ''

                exp_row = [[
                    Paragraph(f'<b>{role}</b>', self.styles['cv_entry_title']),
                    Paragraph(duration, ParagraphStyle(
                        'dur', fontName='Helvetica-Oblique', fontSize=8.5,
                        textColor=GRAY_DARK, alignment=TA_RIGHT)),
                ]]
                exp_t = Table(exp_row, colWidths=[None, 3.5 * cm])
                exp_t.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
                    ('TOPPADDING', (0, 0), (-1, -1), 2),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
                ]))
                story.append(exp_t)
                story.append(self._p(company, 'cv_entry_subtitle'))

                if description:
                    if isinstance(description, list):
                        for item in description:
                            story.append(Paragraph(f'• {item}', self.styles['cv_bullet']))
                    else:
                        items = [d.strip() for d in str(description).split('\n') if d.strip()]
                        if len(items) > 1:
                            for item in items:
                                story.append(Paragraph(f'• {item}', self.styles['cv_bullet']))
                        else:
                            story.append(Paragraph(f'• {description}', self.styles['cv_bullet']))
                story.append(self._spacer(4))

        # ── Habilidades técnicas ──
        hard_skills = perfil.get('hard_skills') or gemini.get('hard_skills') or []
        if hard_skills:
            story.append(self._p('HABILIDADES TÉCNICAS', 'cv_section'))
            story.append(self._hr(thickness=0.4))
            hs = hard_skills if isinstance(hard_skills, list) else [str(hard_skills)]
            story.append(self._p(', '.join(hs), 'cv_skills'))
            story.append(self._spacer(4))

        # ── Habilidades blandas ──
        soft_skills = perfil.get('soft_skills') or gemini.get('soft_skills') or []
        if soft_skills:
            story.append(self._p('HABILIDADES BLANDAS', 'cv_section'))
            story.append(self._hr(thickness=0.4))
            ss = soft_skills if isinstance(soft_skills, list) else [str(soft_skills)]
            story.append(self._p(', '.join(ss), 'cv_skills'))
            story.append(self._spacer(4))

        # ── Idiomas ──
        languages = perfil.get('languages') or gemini.get('languages') or []
        if languages:
            story.append(self._p('IDIOMAS', 'cv_section'))
            story.append(self._hr(thickness=0.4))
            lg = languages if isinstance(languages, list) else [str(languages)]
            story.append(self._p(', '.join(lg), 'cv_skills'))

        story.append(PageBreak())
        return story

    # ─────────────────────────────────────────
    #  MÉTODO PRINCIPAL
    # ─────────────────────────────────────────
    def generate_report(
        self,
        oferta: dict,
        candidatos: list,
        total_postulantes: int,
        top_n: int,
    ) -> bytes:
        """
        Genera el PDF completo del informe de evaluación de candidatos.

        Args:
            oferta: Datos completos de la oferta laboral (incluye institution_name, weights, thresholds, etc.)
            candidatos: Lista de candidatos con 'perfil' y 'gemini_extraction' incluidos
            total_postulantes: Total de postulantes registrados para esta oferta
            top_n: Cantidad de candidatos incluidos en el ranking

        Returns:
            bytes del PDF generado
        """
        buffer = BytesIO()
        ref = self._gen_ref()

        annex_letters   = ANNEX_LETTERS[:len(candidatos)]
        annex_short_refs = [f'Anexo {l}' for l in annex_letters]

        first_page_cb, later_pages_cb = self._make_callbacks(ref, oferta.get('titulo', ''))

        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=2.5 * cm,
            leftMargin=2.5 * cm,
            topMargin=2.8 * cm,
            bottomMargin=2.5 * cm,
            title=f'Informe de Evaluación — {oferta.get("titulo", "")}',
            author='Sistema de Evaluación de Perfiles Profesionales — EMI',
            subject='Informe de Evaluación de Candidatos',
        )

        story = []
        story += self._build_cover(oferta, ref)
        story += self._build_summary(oferta, candidatos, total_postulantes, top_n, annex_short_refs)
        story += self._build_oferta_info(oferta)
        story += self._build_methodology(oferta)
        story += self._build_statistics(candidatos, total_postulantes, annex_short_refs)
        story += self._build_ranking(candidatos, annex_short_refs)
        for letter, candidato in zip(annex_letters, candidatos):
            story += self._build_cv_annex(candidato, letter)

        doc.build(story, onFirstPage=first_page_cb, onLaterPages=later_pages_cb)
        return buffer.getvalue()


# ─────────────────────────────────────────
#  Singleton
# ─────────────────────────────────────────
_pdf_service: PDFReportService | None = None


def get_pdf_report_service() -> PDFReportService:
    global _pdf_service
    if _pdf_service is None:
        _pdf_service = PDFReportService()
    return _pdf_service
