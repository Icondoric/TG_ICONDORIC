============================================================
REPORTE DE EVALUACION DEL MODELO
============================================================

INFORMACION DEL MODELO
----------------------------------------
Tipo: Ridge Regression
Alpha (regularizacion): 0.01
Normalizacion: Si
Intercepto: 0.4731
Ejemplos evaluados: 1000

METRICAS DE REGRESION
----------------------------------------
R2 Score:  0.7996
MSE:       0.0084
RMSE:      0.0918
MAE:       0.0736
MAPE:      24.91%

Media de residuos:     0.001021
Std de residuos:       0.0918

Interpretacion R2: Bueno - El modelo tiene buen poder predictivo

METRICAS DE CLASIFICACION
----------------------------------------
Accuracy: 0.7710 (77.1%)

Precision por clase:
  NO_APTO        : 0.8680
  CONSIDERADO    : 0.5879
  APTO           : 0.8706

Recall por clase:
  NO_APTO        : 0.8500
  CONSIDERADO    : 0.7034
  APTO           : 0.5692

F1-Score por clase:
  NO_APTO        : 0.8589
  CONSIDERADO    : 0.6405
  APTO           : 0.6884

F1-Score Weighted: 0.7734

Distribucion de clases (real vs predicho):
  NO_APTO        :   580 real vs   568 predicho
  CONSIDERADO    :   290 real vs   347 predicho
  APTO           :   130 real vs    85 predicho

Matriz de Confusion:
                  Predicho
                  NO_A  CONS  APTO
  Real NO_A      493    87     0
  Real CONS       75   204    11
  Real APTO        0    56    74

IMPORTANCIA DE FEATURES (Top 10)
----------------------------------------
 1. interaction_edu               : 0.1923 #######
 2. interaction_hard              : 0.1660 ######
 3. interaction_lang              : 0.1569 ######
 4. interaction_soft              : 0.1502 ######
 5. interaction_exp               : 0.1279 #####
 6. experience_delta              : 0.0368 #
 7. inst_weight_lang              : 0.0347 #
 8. min_required_years            : 0.0265 #
 9. inst_weight_exp               : 0.0263 #
10. total_experience_years        : 0.0255 #

VERIFICACION DE OBJETIVOS
----------------------------------------
  R2 >= 0.75          : CUMPLE     (valor: 0.7996)
  RMSE <= 0.17        : CUMPLE     (valor: 0.0918)
  MAE <= 0.12         : CUMPLE     (valor: 0.0736)
  Accuracy >= 0.80    : NO CUMPLE  (valor: 0.7710)

============================================================
RESULTADO: 3/4 OBJETIVOS CUMPLIDOS
============================================================

============================================================
COMPARACION CON BASELINES
============================================================

Modelo          | R2 Score | RMSE    | MAE
--------------------------------------------------
Ridge           | 0.7996   | 0.0918 | 0.0736
Baseline Media  | -0.0038   | 0.2054 | 0.1677
Baseline Mediana| -0.0002   | 0.2050 | 0.1671
Linear Reg      | 0.7985   | 0.0920 | 0.0738

Mejora vs Baselines:
  vs Media:  R2 +0.8035, RMSE -0.1136
  vs Mediana: R2 +0.7998, RMSE -0.1133

============================================================
VISUALIZACIONES GENERADAS
============================================================

  - feature_importance.png: Importancia de features (coeficientes)
  - predictions_vs_actual.png: Predicciones vs valores reales
  - residuals_distribution.png: Distribucion de residuos
  - confusion_matrix.png: Matriz de confusion 3x3
  - score_distribution_by_class.png: Boxplots por clase
  - cv_scores_distribution.png: Scores de Cross-Validation
  - learning_curve.png: Curva de aprendizaje
  - coefficients_heatmap.png: Mapa de calor de coeficientes