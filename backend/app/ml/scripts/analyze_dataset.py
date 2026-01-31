"""
Dataset Analysis Script
Analiza el dataset sintetico generado
"""

import os
import sys

# Agregar el directorio raiz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

import pandas as pd
import numpy as np

# Intentar importar matplotlib (opcional)
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    PLOTTING_AVAILABLE = True
except ImportError:
    PLOTTING_AVAILABLE = False
    print("Warning: matplotlib/seaborn no disponibles. Visualizaciones deshabilitadas.")


def load_dataset(filepath: str = None) -> pd.DataFrame:
    """Carga el dataset"""
    if filepath is None:
        # Buscar en la carpeta training_data
        current_dir = os.path.dirname(__file__)
        filepath = os.path.join(current_dir, '..', 'data', 'training_data', 'synthetic_dataset.csv')

    df = pd.read_csv(filepath)
    print(f"Dataset cargado: {len(df)} ejemplos, {len(df.columns)} columnas")
    return df


def analyze_distribution(df: pd.DataFrame):
    """Analiza la distribucion de scores y clasificaciones"""
    print("\n" + "="*60)
    print("ANALISIS DE DISTRIBUCION")
    print("="*60)

    # Distribucion de match_score
    print(f"\n1. Match Score (variable objetivo):")
    print(f"   Media: {df['match_score'].mean():.3f}")
    print(f"   Mediana: {df['match_score'].median():.3f}")
    print(f"   Desviacion estandar: {df['match_score'].std():.3f}")
    print(f"   Minimo: {df['match_score'].min():.3f}")
    print(f"   Maximo: {df['match_score'].max():.3f}")

    # Quartiles
    print(f"\n   Quartiles:")
    print(f"     Q1 (25%): {df['match_score'].quantile(0.25):.3f}")
    print(f"     Q2 (50%): {df['match_score'].quantile(0.50):.3f}")
    print(f"     Q3 (75%): {df['match_score'].quantile(0.75):.3f}")

    # Distribucion de clasificaciones
    print(f"\n2. Clasificaciones:")
    class_dist = df['classification'].value_counts(normalize=True).sort_index()
    for cls, ratio in class_dist.items():
        count = df['classification'].value_counts()[cls]
        print(f"   {cls:15s}: {ratio*100:5.1f}% ({count:4d} ejemplos)")

    # Verificar balance
    target_dist = {'APTO': 0.40, 'CONSIDERADO': 0.35, 'NO_APTO': 0.25}
    print(f"\n3. Comparacion con distribucion objetivo:")
    for cls in ['APTO', 'CONSIDERADO', 'NO_APTO']:
        actual = class_dist.get(cls, 0)
        target = target_dist[cls]
        diff = actual - target
        print(f"   {cls:15s}: {actual*100:5.1f}% (objetivo: {target*100:.1f}%, diff: {diff*100:+.1f}%)")


def analyze_features(df: pd.DataFrame):
    """Analiza estadisticas de features"""
    print("\n" + "="*60)
    print("ANALISIS DE FEATURES")
    print("="*60)

    # Features del CV (primeras 5 columnas)
    cv_features = df.columns[:5]
    print(f"\n1. CV Scores (debe estar en [0-1]):")
    for feat in cv_features:
        print(f"   {feat:25s}: mean={df[feat].mean():.3f}, std={df[feat].std():.3f}, "
              f"min={df[feat].min():.3f}, max={df[feat].max():.3f}")

    # Pesos institucionales (columnas 5-9)
    weight_features = df.columns[5:10]
    print(f"\n2. Institutional Weights (deben sumar ~1.0):")
    for feat in weight_features:
        print(f"   {feat:25s}: mean={df[feat].mean():.3f}, std={df[feat].std():.3f}")

    # Verificar que pesos sumen 1.0
    weight_sum = df[weight_features].sum(axis=1)
    print(f"\n   Suma de pesos: mean={weight_sum.mean():.3f}, min={weight_sum.min():.3f}, max={weight_sum.max():.3f}")

    if abs(weight_sum.mean() - 1.0) > 0.01:
        print(f"   WARNING: Pesos no suman 1.0 en promedio")
    else:
        print(f"   OK: Pesos suman ~1.0")

    # Context features
    context_features = ['total_experience_years', 'min_required_years', 'experience_delta']
    print(f"\n3. Context Features:")
    for feat in context_features:
        if feat in df.columns:
            print(f"   {feat:25s}: mean={df[feat].mean():.3f}, std={df[feat].std():.3f}")


def analyze_correlations(df: pd.DataFrame):
    """Analiza correlaciones entre features y target"""
    print("\n" + "="*60)
    print("ANALISIS DE CORRELACIONES")
    print("="*60)

    # Correlacion con match_score
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    correlations = df[numeric_cols].corr()['match_score'].drop('match_score').sort_values(ascending=False)

    print(f"\nTop 10 features mas correlacionadas con match_score:")
    for i, (feat, corr) in enumerate(correlations.head(10).items(), 1):
        print(f"   {i:2d}. {feat:30s}: {corr:+.3f}")

    print(f"\nTop 5 features menos correlacionadas:")
    for i, (feat, corr) in enumerate(correlations.tail(5).items(), 1):
        print(f"   {i:2d}. {feat:30s}: {corr:+.3f}")


def check_data_quality(df: pd.DataFrame):
    """Verifica calidad de los datos"""
    print("\n" + "="*60)
    print("VERIFICACION DE CALIDAD")
    print("="*60)

    issues = []

    # 1. Valores nulos
    null_counts = df.isnull().sum()
    if null_counts.sum() > 0:
        issues.append("Valores nulos encontrados")
        print(f"\nX Valores nulos:")
        for col, count in null_counts[null_counts > 0].items():
            print(f"   {col}: {count}")
    else:
        print(f"\nOK Sin valores nulos")

    # 2. Valores fuera de rango [0-1] para scores
    score_cols = df.columns[:5]  # Primeros 5 son scores
    out_of_range = False
    for col in score_cols:
        if (df[col] < 0).any() or (df[col] > 1).any():
            issues.append(f"Valores fuera de rango en {col}")
            print(f"X {col} tiene valores fuera de [0-1]")
            out_of_range = True

    if not out_of_range:
        print(f"OK Todos los scores en rango [0-1]")

    # 3. Duplicados
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        issues.append(f"{duplicates} filas duplicadas")
        print(f"\nWARNING {duplicates} filas duplicadas encontradas")
    else:
        print(f"\nOK Sin duplicados")

    # 4. Variabilidad
    low_var_cols = df.select_dtypes(include=[np.number]).var()
    low_var_cols = low_var_cols[low_var_cols < 0.001].index.tolist()
    if low_var_cols:
        issues.append("Columnas con varianza muy baja")
        print(f"\nWARNING Columnas con varianza < 0.001: {low_var_cols}")
    else:
        print(f"OK Variabilidad adecuada en todas las columnas")

    # Resumen
    if not issues:
        print(f"\n{'='*60}")
        print(f"DATASET PASA TODAS LAS VERIFICACIONES DE CALIDAD")
        print(f"{'='*60}")
    else:
        print(f"\n{'='*60}")
        print(f"DATASET TIENE {len(issues)} PROBLEMAS:")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
        print(f"{'='*60}")

    return len(issues) == 0


def create_visualizations(df: pd.DataFrame, output_dir: str = None):
    """Crea visualizaciones del dataset"""
    if not PLOTTING_AVAILABLE:
        print("\nVisualizaciones no disponibles (matplotlib no instalado)")
        return

    if output_dir is None:
        current_dir = os.path.dirname(__file__)
        output_dir = os.path.join(current_dir, '..', 'visualizations')

    os.makedirs(output_dir, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"GENERANDO VISUALIZACIONES")
    print(f"{'='*60}")

    # Configurar estilo
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (10, 6)

    # 1. Distribucion de match_score
    plt.figure(figsize=(10, 6))
    plt.hist(df['match_score'], bins=50, edgecolor='black', alpha=0.7)
    plt.axvline(df['match_score'].mean(), color='red', linestyle='--', label=f'Media: {df["match_score"].mean():.3f}')
    plt.axvline(df['match_score'].median(), color='green', linestyle='--', label=f'Mediana: {df["match_score"].median():.3f}')
    plt.xlabel('Match Score')
    plt.ylabel('Frecuencia')
    plt.title('Distribucion de Match Score')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'{output_dir}/distribution_match_score.png', dpi=150)
    print(f"   Guardado: {output_dir}/distribution_match_score.png")
    plt.close()

    # 2. Distribucion por clasificacion
    plt.figure(figsize=(8, 6))
    class_counts = df['classification'].value_counts()
    colors = {'APTO': 'green', 'CONSIDERADO': 'orange', 'NO_APTO': 'red'}
    bars = plt.bar(class_counts.index, class_counts.values,
                   color=[colors.get(c, 'blue') for c in class_counts.index],
                   edgecolor='black', alpha=0.7)
    plt.xlabel('Clasificacion')
    plt.ylabel('Cantidad')
    plt.title('Distribucion de Clasificaciones')
    # Aniadir porcentajes
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height}\n({height/len(df)*100:.1f}%)',
                ha='center', va='bottom')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/distribution_classification.png', dpi=150)
    print(f"   Guardado: {output_dir}/distribution_classification.png")
    plt.close()

    # 3. Correlacion con match_score
    plt.figure(figsize=(10, 8))
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    correlations = df[numeric_cols].corr()['match_score'].drop('match_score').sort_values()
    correlations.plot(kind='barh', color=['red' if x < 0 else 'green' for x in correlations])
    plt.xlabel('Correlacion con Match Score')
    plt.title('Correlacion de Features con Match Score')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/correlations.png', dpi=150)
    print(f"   Guardado: {output_dir}/correlations.png")
    plt.close()

    print(f"\nVisualizaciones generadas en: {output_dir}/")


def main():
    """Funcion principal"""
    print("="*60)
    print("ANALISIS DE DATASET SINTETICO")
    print("="*60)

    # Cargar dataset
    df = load_dataset()

    # Analisis
    analyze_distribution(df)
    analyze_features(df)
    analyze_correlations(df)
    quality_ok = check_data_quality(df)

    # Visualizaciones (opcional)
    try:
        create_visualizations(df)
    except Exception as e:
        print(f"\nError generando visualizaciones: {e}")

    print(f"\n{'='*60}")
    print(f"ANALISIS COMPLETADO")
    print(f"{'='*60}")

    return df, quality_ok


if __name__ == "__main__":
    df, quality_ok = main()
