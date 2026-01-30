"""
Dataset Analysis Script
Analiza el dataset sintético generado
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


def load_dataset(filepath: str = 'synthetic_dataset.csv') -> pd.DataFrame:
    """Carga el dataset"""
    df = pd.read_csv(filepath)
    print(f"✅ Dataset cargado: {len(df)} ejemplos, {len(df.columns)} columnas")
    return df


def analyze_distribution(df: pd.DataFrame):
    """Analiza la distribución de scores y clasificaciones"""
    print("\n" + "="*60)
    print("📊 ANÁLISIS DE DISTRIBUCIÓN")
    print("="*60)
    
    # Distribución de match_score
    print(f"\n1. Match Score (variable objetivo):")
    print(f"   Media: {df['match_score'].mean():.3f}")
    print(f"   Mediana: {df['match_score'].median():.3f}")
    print(f"   Desviación estándar: {df['match_score'].std():.3f}")
    print(f"   Mínimo: {df['match_score'].min():.3f}")
    print(f"   Máximo: {df['match_score'].max():.3f}")
    
    # Quartiles
    print(f"\n   Quartiles:")
    print(f"     Q1 (25%): {df['match_score'].quantile(0.25):.3f}")
    print(f"     Q2 (50%): {df['match_score'].quantile(0.50):.3f}")
    print(f"     Q3 (75%): {df['match_score'].quantile(0.75):.3f}")
    
    # Distribución de clasificaciones
    print(f"\n2. Clasificaciones:")
    class_dist = df['classification'].value_counts(normalize=True).sort_index()
    for cls, ratio in class_dist.items():
        count = df['classification'].value_counts()[cls]
        print(f"   {cls:15s}: {ratio*100:5.1f}% ({count:4d} ejemplos)")
    
    # Verificar balance
    target_dist = {'APTO': 0.40, 'CONSIDERADO': 0.35, 'NO_APTO': 0.25}
    print(f"\n3. Comparación con distribución objetivo:")
    for cls in ['APTO', 'CONSIDERADO', 'NO_APTO']:
        actual = class_dist.get(cls, 0)
        target = target_dist[cls]
        diff = actual - target
        print(f"   {cls:15s}: {actual*100:5.1f}% (objetivo: {target*100:.1f}%, diff: {diff*100:+.1f}%)")


def analyze_features(df: pd.DataFrame):
    """Analiza estadísticas de features"""
    print("\n" + "="*60)
    print("📈 ANÁLISIS DE FEATURES")
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
        print(f"   ⚠️ WARNING: Pesos no suman 1.0 en promedio")
    else:
        print(f"   ✅ OK: Pesos suman ~1.0")
    
    # Context features (últimas 3 columnas antes de match_score)
    context_features = ['total_experience_years', 'min_required_years', 'experience_delta']
    print(f"\n3. Context Features:")
    for feat in context_features:
        if feat in df.columns:
            print(f"   {feat:25s}: mean={df[feat].mean():.3f}, std={df[feat].std():.3f}")


def analyze_correlations(df: pd.DataFrame):
    """Analiza correlaciones entre features y target"""
    print("\n" + "="*60)
    print("🔗 ANÁLISIS DE CORRELACIONES")
    print("="*60)
    
    # Correlación con match_score
    correlations = df.corr()['match_score'].drop('match_score').sort_values(ascending=False)
    
    print(f"\nTop 10 features más correlacionadas con match_score:")
    for i, (feat, corr) in enumerate(correlations.head(10).items(), 1):
        print(f"   {i:2d}. {feat:30s}: {corr:+.3f}")
    
    print(f"\nTop 5 features menos correlacionadas:")
    for i, (feat, corr) in enumerate(correlations.tail(5).items(), 1):
        print(f"   {i:2d}. {feat:30s}: {corr:+.3f}")


def check_data_quality(df: pd.DataFrame):
    """Verifica calidad de los datos"""
    print("\n" + "="*60)
    print("✅ VERIFICACIÓN DE CALIDAD")
    print("="*60)
    
    issues = []
    
    # 1. Valores nulos
    null_counts = df.isnull().sum()
    if null_counts.sum() > 0:
        issues.append("Valores nulos encontrados")
        print(f"\n❌ Valores nulos:")
        for col, count in null_counts[null_counts > 0].items():
            print(f"   {col}: {count}")
    else:
        print(f"\n✅ Sin valores nulos")
    
    # 2. Valores fuera de rango [0-1] para scores
    score_cols = df.columns[:5]  # Primeros 5 son scores
    for col in score_cols:
        if (df[col] < 0).any() or (df[col] > 1).any():
            issues.append(f"Valores fuera de rango en {col}")
            print(f"❌ {col} tiene valores fuera de [0-1]")
    
    if not issues:
        print(f"✅ Todos los scores en rango [0-1]")
    
    # 3. Duplicados
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        issues.append(f"{duplicates} filas duplicadas")
        print(f"\n⚠️ {duplicates} filas duplicadas encontradas")
    else:
        print(f"\n✅ Sin duplicados")
    
    # 4. Variabilidad
    low_var_cols = df.var()[df.var() < 0.001].index.tolist()
    if low_var_cols:
        issues.append("Columnas con varianza muy baja")
        print(f"\n⚠️ Columnas con varianza < 0.001: {low_var_cols}")
    else:
        print(f"✅ Variabilidad adecuada en todas las columnas")
    
    # Resumen
    if not issues:
        print(f"\n{'='*60}")
        print(f"✅ DATASET PASA TODAS LAS VERIFICACIONES DE CALIDAD")
        print(f"{'='*60}")
    else:
        print(f"\n{'='*60}")
        print(f"⚠️ DATASET TIENE {len(issues)} PROBLEMAS:")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
        print(f"{'='*60}")


def create_visualizations(df: pd.DataFrame, output_dir: str = 'visualizations'):
    """Crea visualizaciones del dataset"""
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n{'='*60}")
    print(f"📊 GENERANDO VISUALIZACIONES")
    print(f"{'='*60}")
    
    # Configurar estilo
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (10, 6)
    
    # 1. Distribución de match_score
    plt.figure(figsize=(10, 6))
    plt.hist(df['match_score'], bins=50, edgecolor='black', alpha=0.7)
    plt.axvline(df['match_score'].mean(), color='red', linestyle='--', label=f'Media: {df["match_score"].mean():.3f}')
    plt.axvline(df['match_score'].median(), color='green', linestyle='--', label=f'Mediana: {df["match_score"].median():.3f}')
    plt.xlabel('Match Score')
    plt.ylabel('Frecuencia')
    plt.title('Distribución de Match Score')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'{output_dir}/distribution_match_score.png', dpi=150)
    print(f"   ✅ Guardado: {output_dir}/distribution_match_score.png")
    plt.close()
    
    # 2. Distribución por clasificación
    plt.figure(figsize=(8, 6))
    class_counts = df['classification'].value_counts()
    colors = {'APTO': 'green', 'CONSIDERADO': 'orange', 'NO_APTO': 'red'}
    bars = plt.bar(class_counts.index, class_counts.values, 
                   color=[colors[c] for c in class_counts.index],
                   edgecolor='black', alpha=0.7)
    plt.xlabel('Clasificación')
    plt.ylabel('Cantidad')
    plt.title('Distribución de Clasificaciones')
    # Añadir porcentajes
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height}\n({height/len(df)*100:.1f}%)',
                ha='center', va='bottom')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/distribution_classification.png', dpi=150)
    print(f"   ✅ Guardado: {output_dir}/distribution_classification.png")
    plt.close()
    
    # 3. Correlación con match_score
    plt.figure(figsize=(10, 8))
    correlations = df.corr()['match_score'].drop('match_score').sort_values()
    correlations.plot(kind='barh', color=['red' if x < 0 else 'green' for x in correlations])
    plt.xlabel('Correlación con Match Score')
    plt.title('Correlación de Features con Match Score')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/correlations.png', dpi=150)
    print(f"   ✅ Guardado: {output_dir}/correlations.png")
    plt.close()
    
    # 4. Boxplot de scores por clasificación
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    cv_features = df.columns[:5]
    
    for i, feat in enumerate(cv_features):
        ax = axes[i//3, i%3]
        df.boxplot(column=feat, by='classification', ax=ax)
        ax.set_title(feat.replace('_', ' ').title())
        ax.set_xlabel('')
        plt.sca(ax)
        plt.xticks(rotation=45)
    
    # Eliminar subplot extra
    fig.delaxes(axes[1, 2])
    
    plt.suptitle('Distribución de CV Scores por Clasificación', y=1.02)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/scores_by_classification.png', dpi=150)
    print(f"   ✅ Guardado: {output_dir}/scores_by_classification.png")
    plt.close()
    
    print(f"\n✅ Visualizaciones generadas en: {output_dir}/")


def main():
    """Función principal"""
    print("="*60)
    print("ANÁLISIS DE DATASET SINTÉTICO")
    print("="*60)
    
    # Cargar dataset
    df = load_dataset('synthetic_dataset.csv')
    
    # Análisis
    analyze_distribution(df)
    analyze_features(df)
    analyze_correlations(df)
    check_data_quality(df)
    
    # Visualizaciones
    try:
        create_visualizations(df)
    except Exception as e:
        print(f"\n⚠️ Error generando visualizaciones: {e}")
        print(f"   (Puede que matplotlib no esté disponible)")
    
    print(f"\n{'='*60}")
    print(f"✅ ANÁLISIS COMPLETADO")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
