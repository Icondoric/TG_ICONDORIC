"""
CV PDF Service — Generación de Currículum Vítae en formato Harvard.

Produce un documento A4 con:
  - Nombre y datos de contacto centrados
  - Línea divisoria navy
  - Perfil profesional (si existe en extracción Gemini)
  - Formación académica (ordenada por año desc)
  - Experiencia profesional (con bullets de descripción)
  - Habilidades técnicas
  - Habilidades blandas
  - Idiomas
  - Pie de página institucional EMI
"""

import logging
from datetime import datetime
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────
#  Paleta corporativa (igual que pdf_report_service)
# ─────────────────────────────────────────
NAVY       = colors.HexColor('#1B3A6B')
NAVY_MED   = colors.HexColor('#2C5282')
GRAY_DARK  = colors.HexColor('#4A5568')
GRAY_MED   = colors.HexColor('#E2E8F0')
WHITE      = colors.white
BLACK      = colors.black


class CVPdfService:
    """Genera el Currículum Vítae de un usuario en formato Harvard (A4)."""

    PAGE_W, PAGE_H = A4

    def __init__(self):
        self.styles = self._build_styles()

    # ─────────────────────────────────────────
    #  Estilos tipográficos
    # ─────────────────────────────────────────
    def _build_styles(self) -> dict:
        return {
            'name': ParagraphStyle(
                'name', fontName='Helvetica-Bold', fontSize=20,
                textColor=NAVY, alignment=TA_CENTER,
                spaceAfter=10, letterSpacing=1.5,
            ),
            'contact': ParagraphStyle(
                'contact', fontName='Helvetica', fontSize=9,
                textColor=GRAY_DARK, alignment=TA_CENTER, spaceAfter=8,
            ),
            'section': ParagraphStyle(
                'section', fontName='Helvetica-Bold', fontSize=10,
                textColor=NAVY, spaceBefore=14, spaceAfter=2, letterSpacing=2,
            ),
            'entry_title': ParagraphStyle(
                'entry_title', fontName='Helvetica-Bold', fontSize=9.5,
                textColor=BLACK, spaceAfter=1,
            ),
            'entry_sub': ParagraphStyle(
                'entry_sub', fontName='Helvetica-Oblique', fontSize=9,
                textColor=GRAY_DARK, spaceAfter=3,
            ),
            'body': ParagraphStyle(
                'body', fontName='Helvetica', fontSize=9.5,
                textColor=BLACK, leading=14, spaceAfter=4,
            ),
            'bullet': ParagraphStyle(
                'bullet', fontName='Helvetica', fontSize=9,
                textColor=BLACK, leftIndent=12, spaceAfter=1, leading=12,
            ),
            'skills': ParagraphStyle(
                'skills', fontName='Helvetica', fontSize=9.5,
                textColor=BLACK, leading=14, spaceAfter=4,
            ),
            'footer': ParagraphStyle(
                'footer', fontName='Helvetica', fontSize=7.5,
                textColor=GRAY_DARK, alignment=TA_CENTER,
            ),
        }

    # ─────────────────────────────────────────
    #  Helpers de flowables
    # ─────────────────────────────────────────
    def _hr(self, color=GRAY_MED, thickness=0.5):
        return HRFlowable(
            width='100%', thickness=thickness,
            color=color, spaceAfter=6, spaceBefore=2,
        )

    def _hr_navy(self):
        return HRFlowable(
            width='100%', thickness=1.5,
            color=NAVY, spaceAfter=10, spaceBefore=4,
        )

    def _spacer(self, h=6):
        return Spacer(1, h)

    def _p(self, text, style_key):
        return Paragraph(str(text) if text else '', self.styles[style_key])

    def _section_header(self, text: str) -> list:
        return [
            self._p(text.upper(), 'section'),
            self._hr(thickness=0.4),
        ]

    def _two_col_row(self, left_para, right_para, right_width=2.2 * cm) -> Table:
        """Fila con texto izquierdo y texto derecho (año / duración)."""
        t = Table([[left_para, right_para]], colWidths=[None, right_width])
        t.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
        ]))
        return t

    # ─────────────────────────────────────────
    #  Callbacks header / footer
    # ─────────────────────────────────────────
    def _make_callbacks(self, ref: str):
        pw, ph = self.PAGE_W, self.PAGE_H

        def _first_page(canvas, doc):
            pass  # Sin decoración en primera página

        def _later_pages(canvas, doc):
            canvas.saveState()
            canvas.setStrokeColor(GRAY_MED)
            canvas.setLineWidth(0.4)
            canvas.line(2.5 * cm, 1.8 * cm, pw - 2.5 * cm, 1.8 * cm)
            canvas.setFont('Helvetica', 7)
            canvas.setFillColor(GRAY_DARK)
            canvas.drawCentredString(pw / 2, 1.3 * cm, f'Página {doc.page}')
            canvas.drawRightString(pw - 2.5 * cm, 1.3 * cm, ref)
            canvas.restoreState()

        return _first_page, _later_pages

    # ─────────────────────────────────────────
    #  MÉTODO PRINCIPAL
    # ─────────────────────────────────────────
    def generate(self, profile: dict) -> bytes:
        """
        Genera el CV PDF del usuario.

        Args:
            profile: Diccionario completo del perfil (campos de la tabla user_profiles
                     incluyendo gemini_extraction).

        Returns:
            bytes del PDF generado.
        """
        buffer = BytesIO()
        date_str = datetime.now().strftime('%Y%m%d')
        nombre_raw = profile.get('nombre_completo') or 'CV'
        ref = f'CV-EMI-{date_str}'

        first_cb, later_cb = self._make_callbacks(ref)

        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=2.5 * cm,
            leftMargin=2.5 * cm,
            topMargin=2.5 * cm,
            bottomMargin=2.5 * cm,
            title=f'Currículum Vítae — {nombre_raw}',
            author='Sistema de Evaluación de Perfiles Profesionales — EMI',
            subject='Currículum Vítae',
        )

        story = self._build_story(profile)
        doc.build(story, onFirstPage=first_cb, onLaterPages=later_cb)
        return buffer.getvalue()

    def _build_story(self, profile: dict) -> list:
        story = []
        gemini = profile.get('gemini_extraction') or {}
        personal = gemini.get('personal_info') or {}

        nombre = profile.get('nombre_completo') or 'Nombre no disponible'

        # ── Nombre ──────────────────────────────────────────
        story.append(self._spacer(4))
        story.append(self._p(nombre.upper(), 'name'))

        # ── Contacto en una línea ────────────────────────────
        contact_parts = []
        if profile.get('email_contacto'):
            contact_parts.append(profile['email_contacto'])
        if profile.get('telefono'):
            contact_parts.append(profile['telefono'])
        if profile.get('direccion'):
            contact_parts.append(profile['direccion'])
        elif personal.get('address'):
            contact_parts.append(personal['address'])
        if profile.get('nacionalidad'):
            contact_parts.append(profile['nacionalidad'])
        if contact_parts:
            story.append(self._p(' &nbsp;|&nbsp; '.join(contact_parts), 'contact'))

        # ── Línea divisoria navy principal ───────────────────
        story.append(self._hr_navy())

        # ── PERFIL PROFESIONAL ───────────────────────────────
        summary = personal.get('summary') or ''
        if summary:
            story += self._section_header('Perfil Profesional')
            story.append(self._p(str(summary), 'body'))
            story.append(self._spacer(4))

        # ── FORMACIÓN ACADÉMICA ──────────────────────────────
        education = gemini.get('education') or []
        education_level = profile.get('education_level') or ''

        if education or education_level:
            story += self._section_header('Formación Académica')

            if education:
                sorted_edu = sorted(
                    education,
                    key=lambda e: str(e.get('year', '0')),
                    reverse=True,
                )
                for edu in sorted_edu:
                    degree = edu.get('degree') or edu.get('title') or '—'
                    institution = edu.get('institution') or '—'
                    year = str(edu.get('year') or '')
                    field = edu.get('field') or edu.get('area') or ''
                    label = f'<b>{degree}</b>' + (f' — {field}' if field else '')

                    story.append(self._two_col_row(
                        Paragraph(label, self.styles['entry_title']),
                        Paragraph(year, ParagraphStyle(
                            'yr', fontName='Helvetica-Oblique', fontSize=9,
                            textColor=GRAY_DARK, alignment=TA_RIGHT)),
                    ))
                    story.append(self._p(institution, 'entry_sub'))
            else:
                # Solo nivel educativo sin detalle de Gemini
                story.append(self._two_col_row(
                    Paragraph(f'<b>{education_level}</b>', self.styles['entry_title']),
                    Paragraph('Nivel más alto', ParagraphStyle(
                        'lvl', fontName='Helvetica-Oblique', fontSize=9,
                        textColor=GRAY_DARK, alignment=TA_RIGHT)),
                    right_width=3.5 * cm,
                ))
            story.append(self._spacer(4))

        # ── EXPERIENCIA PROFESIONAL ──────────────────────────
        experience = gemini.get('experience') or []
        experience_years = float(profile.get('experience_years') or 0)

        if experience or experience_years:
            story += self._section_header('Experiencia Profesional')

            if experience:
                for exp in experience:
                    role = (
                        exp.get('role') or exp.get('position') or
                        exp.get('title') or '—'
                    )
                    company = exp.get('company') or exp.get('organization') or '—'
                    duration = exp.get('duration') or exp.get('period') or ''
                    description = exp.get('description') or exp.get('responsibilities') or ''

                    story.append(self._two_col_row(
                        Paragraph(f'<b>{role}</b>', self.styles['entry_title']),
                        Paragraph(duration, ParagraphStyle(
                            'dur', fontName='Helvetica-Oblique', fontSize=8.5,
                            textColor=GRAY_DARK, alignment=TA_RIGHT)),
                        right_width=3.5 * cm,
                    ))
                    story.append(self._p(company, 'entry_sub'))

                    if description:
                        if isinstance(description, list):
                            for item in description:
                                story.append(Paragraph(f'• {item}', self.styles['bullet']))
                        else:
                            items = [d.strip() for d in str(description).split('\n') if d.strip()]
                            for item in (items if len(items) > 1 else [str(description)]):
                                story.append(Paragraph(f'• {item}', self.styles['bullet']))
                    story.append(self._spacer(4))
            else:
                story.append(self._p(
                    f'<b>Experiencia declarada:</b> {int(experience_years)} año(s)', 'body'
                ))
            story.append(self._spacer(2))

        # ── HABILIDADES TÉCNICAS ─────────────────────────────
        hard_skills = profile.get('hard_skills') or gemini.get('hard_skills') or []
        if hard_skills:
            hs = hard_skills if isinstance(hard_skills, list) else [str(hard_skills)]
            story += self._section_header('Habilidades Técnicas')
            story.append(self._p(', '.join(hs), 'skills'))
            story.append(self._spacer(2))

        # ── HABILIDADES BLANDAS ──────────────────────────────
        soft_skills = profile.get('soft_skills') or gemini.get('soft_skills') or []
        if soft_skills:
            ss = soft_skills if isinstance(soft_skills, list) else [str(soft_skills)]
            story += self._section_header('Habilidades Blandas')
            story.append(self._p(', '.join(ss), 'skills'))
            story.append(self._spacer(2))

        # ── IDIOMAS ──────────────────────────────────────────
        languages = profile.get('languages') or gemini.get('languages') or []
        if languages:
            lg = languages if isinstance(languages, list) else [str(languages)]
            story += self._section_header('Idiomas')
            story.append(self._p(', '.join(lg), 'skills'))

        # ── Pie de página ────────────────────────────────────
        story.append(self._spacer(24))
        story.append(self._hr(color=GRAY_MED, thickness=0.4))
        story.append(self._p(
            'Sistema de Evaluación de Perfiles Profesionales — EMI',
            'footer',
        ))

        return story


# ─────────────────────────────────────────
#  Singleton
# ─────────────────────────────────────────
_cv_pdf_service: CVPdfService | None = None


def get_cv_pdf_service() -> CVPdfService:
    global _cv_pdf_service
    if _cv_pdf_service is None:
        _cv_pdf_service = CVPdfService()
    return _cv_pdf_service
