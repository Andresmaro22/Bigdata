import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Usar backend sin GUI
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

# Configurar estilo
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (15, 12)
plt.rcParams['font.size'] = 10

# Leer datos
df = pd.read_csv('datos_sinteticos.csv')
df['fecha_campana'] = pd.to_datetime(df['fecha_campana'])

# Crear figura con subplots
fig = plt.figure(figsize=(20, 16))

# 1. Revenue y Conversiones por Plataforma
ax1 = plt.subplot(3, 3, 1)
platform_metrics = df.groupby('plataforma').agg({
    'revenue_generado': 'sum',
    'conversiones': 'sum',
    'costo_total': 'sum'
}).reset_index()

x = np.arange(len(platform_metrics))
width = 0.25
bars1 = ax1.bar(x - width, platform_metrics['revenue_generado'], width, label='Revenue', color='#2ecc71')
bars2 = ax1.bar(x, platform_metrics['conversiones']*100, width, label='Conversiones (x100)', color='#3498db')
bars3 = ax1.bar(x + width, platform_metrics['costo_total'], width, label='Costo Total', color='#e74c3c')

ax1.set_xlabel('Plataforma')
ax1.set_ylabel('Valor')
ax1.set_title('Revenue, Conversiones y Costo por Plataforma')
ax1.set_xticks(x)
ax1.set_xticklabels(platform_metrics['plataforma'], rotation=45, ha='right')
ax1.legend()
ax1.grid(axis='y', alpha=0.3)

# 2. ROAS por Plataforma
ax2 = plt.subplot(3, 3, 2)
roas_platform = df.groupby('plataforma')['roas'].mean().sort_values(ascending=False)
colors = ['#2ecc71' if x > 5 else '#f39c12' if x > 2 else '#e74c3c' for x in roas_platform.values]
roas_platform.plot(kind='bar', ax=ax2, color=colors)
ax2.set_title('ROAS Promedio por Plataforma')
ax2.set_xlabel('Plataforma')
ax2.set_ylabel('ROAS')
ax2.axhline(y=2, color='red', linestyle='--', alpha=0.5, label='Umbral Mínimo')
ax2.legend()
ax2.grid(axis='y', alpha=0.3)
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')

# 3. CTR y Conversion Rate por Tipo de Campaña
ax3 = plt.subplot(3, 3, 3)
campaign_metrics = df.groupby('tipo_campana').agg({
    'ctr': 'mean',
    'conversion_rate': 'mean'
}).reset_index()

x = np.arange(len(campaign_metrics))
width = 0.35
ax3_twin = ax3.twinx()
bars1 = ax3.bar(x - width/2, campaign_metrics['ctr'], width, label='CTR Promedio (%)', color='#9b59b6')
bars2 = ax3_twin.bar(x + width/2, campaign_metrics['conversion_rate'], width, label='Conversion Rate (%)', color='#1abc9c')

ax3.set_xlabel('Tipo de Campaña')
ax3.set_ylabel('CTR (%)', color='#9b59b6')
ax3_twin.set_ylabel('Conversion Rate (%)', color='#1abc9c')
ax3.set_title('CTR y Tasa de Conversión por Tipo de Campaña')
ax3.set_xticks(x)
ax3.set_xticklabels(campaign_metrics['tipo_campana'], rotation=45, ha='right')
ax3.tick_params(axis='y', labelcolor='#9b59b6')
ax3_twin.tick_params(axis='y', labelcolor='#1abc9c')
ax3.grid(axis='y', alpha=0.3)

# 4. Distribución de Audiencia Objetivo
ax4 = plt.subplot(3, 3, 4)
audience_dist = df['audiencia_objetivo'].value_counts()
colors_pie = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']
wedges, texts, autotexts = ax4.pie(audience_dist.values, labels=audience_dist.index, autopct='%1.1f%%',
                                     colors=colors_pie, startangle=90)
ax4.set_title('Distribución de Audiencia Objetivo')
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')

# 5. Presupuesto vs Revenue Generado
ax5 = plt.subplot(3, 3, 5)
scatter = ax5.scatter(df['presupuesto_diario'], df['revenue_generado'], 
                     c=df['roas'], cmap='RdYlGn', s=100, alpha=0.6, edgecolors='black')
ax5.set_xlabel('Presupuesto Diario ($)')
ax5.set_ylabel('Revenue Generado ($)')
ax5.set_title('Presupuesto vs Revenue (coloreado por ROAS)')
cbar = plt.colorbar(scatter, ax=ax5)
cbar.set_label('ROAS')
ax5.grid(True, alpha=0.3)

# 6. CPC vs CPA
ax6 = plt.subplot(3, 3, 6)
scatter2 = ax6.scatter(df['cpc'], df['cpa'], 
                      c=df['conversion_rate'], cmap='viridis', s=100, alpha=0.6, edgecolors='black')
ax6.set_xlabel('Costo por Click ($)')
ax6.set_ylabel('Costo por Adquisición ($)')
ax6.set_title('CPC vs CPA (coloreado por Conversion Rate)')
cbar2 = plt.colorbar(scatter2, ax=ax6)
cbar2.set_label('Conversion Rate (%)')
ax6.grid(True, alpha=0.3)

# 7. Engagement Rate por Plataforma (Box Plot)
ax7 = plt.subplot(3, 3, 7)
df_sorted = df.sort_values('plataforma')
bp = ax7.boxplot([df[df['plataforma'] == p]['engagement_rate'].values 
                    for p in df['plataforma'].unique()],
                   labels=df['plataforma'].unique(),
                   patch_artist=True)
for patch, color in zip(bp['boxes'], ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']):
    patch.set_facecolor(color)
ax7.set_xlabel('Plataforma')
ax7.set_ylabel('Engagement Rate (%)')
ax7.set_title('Distribución de Engagement Rate por Plataforma')
plt.setp(ax7.xaxis.get_majorticklabels(), rotation=45, ha='right')
ax7.grid(axis='y', alpha=0.3)

# 8. Conversiones por Audiencia
ax8 = plt.subplot(3, 3, 8)
conversion_by_audience = df.groupby('audiencia_objetivo').agg({
    'conversiones': 'sum',
    'costo_total': 'sum'
}).reset_index()
conversion_by_audience['costo_por_conversion'] = conversion_by_audience['costo_total'] / conversion_by_audience['conversiones']
conversion_by_audience = conversion_by_audience.sort_values('conversiones', ascending=False)

ax8_twin = ax8.twinx()
bars1 = ax8.bar(conversion_by_audience['audiencia_objetivo'], conversion_by_audience['conversiones'], 
                color='#2ecc71', alpha=0.7, label='Total Conversiones')
line = ax8_twin.plot(conversion_by_audience['audiencia_objetivo'], 
                     conversion_by_audience['costo_por_conversion'], 
                     color='#e74c3c', marker='o', linewidth=2, markersize=8, label='Costo/Conversión')

ax8.set_xlabel('Audiencia Objetivo')
ax8.set_ylabel('Total Conversiones', color='#2ecc71')
ax8_twin.set_ylabel('Costo por Conversión ($)', color='#e74c3c')
ax8.set_title('Conversiones y Costo por Conversión por Audiencia')
ax8.tick_params(axis='y', labelcolor='#2ecc71')
ax8_twin.tick_params(axis='y', labelcolor='#e74c3c')
plt.setp(ax8.xaxis.get_majorticklabels(), rotation=45, ha='right')
ax8.grid(axis='y', alpha=0.3)

# 9. Tendencia Temporal de Revenue
ax9 = plt.subplot(3, 3, 9)
daily_revenue = df.groupby('fecha_campana')['revenue_generado'].sum().resample('W').sum()
ax9.plot(daily_revenue.index, daily_revenue.values, marker='o', linewidth=2, 
         color='#2ecc71', markersize=8, label='Revenue Semanal')
ax9.fill_between(daily_revenue.index, daily_revenue.values, alpha=0.3, color='#2ecc71')
ax9.set_xlabel('Fecha')
ax9.set_ylabel('Revenue Generado ($)')
ax9.set_title('Tendencia de Revenue en el Tiempo')
ax9.grid(True, alpha=0.3)
plt.setp(ax9.xaxis.get_majorticklabels(), rotation=45, ha='right')

plt.tight_layout()
plt.savefig('analisis_campanas.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico guardado como 'analisis_campanas.png'")

# Crear un segundo gráfico con análisis de correlación
fig2, ((ax10, ax11), (ax12, ax13)) = plt.subplots(2, 2, figsize=(16, 12))

# 10. Matriz de Correlación
numeric_cols = df.select_dtypes(include=[np.number]).columns
correlation_matrix = df[numeric_cols].corr()
sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0, 
            ax=ax10, cbar_kws={'label': 'Correlación'})
ax10.set_title('Matriz de Correlación - Variables Numéricas')

# 11. Impresiones vs Clicks vs Conversiones (por tipo de campaña)
ax11.set_title('Embudo de Conversión por Tipo de Campaña')
funnel_data = df.groupby('tipo_campana').agg({
    'impresiones': 'sum',
    'clicks': 'sum',
    'conversiones': 'sum'
}).reset_index()

x = np.arange(len(funnel_data))
width = 0.25
ax11.bar(x - width, funnel_data['impresiones']/1000, width, label='Impresiones (÷1000)', color='#3498db')
ax11.bar(x, funnel_data['clicks']/100, width, label='Clicks (÷100)', color='#f39c12')
ax11.bar(x + width, funnel_data['conversiones'], width, label='Conversiones', color='#2ecc71')
ax11.set_xlabel('Tipo de Campaña')
ax11.set_ylabel('Cantidad')
ax11.set_xticks(x)
ax11.set_xticklabels(funnel_data['tipo_campana'], rotation=45, ha='right')
ax11.legend()
ax11.grid(axis='y', alpha=0.3)

# 12. Performance Score por Plataforma
ax12.set_title('Score de Rendimiento Integrado por Plataforma')
platform_performance = df.groupby('plataforma').agg({
    'roas': 'mean',
    'conversion_rate': 'mean',
    'ctr': 'mean',
    'engagement_rate': 'mean'
}).reset_index()

# Normalizar métricas para crear un score (0-100)
for col in ['roas', 'conversion_rate', 'ctr', 'engagement_rate']:
    platform_performance[col + '_norm'] = (platform_performance[col] - platform_performance[col].min()) / \
                                          (platform_performance[col].max() - platform_performance[col].min()) * 100

platform_performance['score'] = platform_performance[['roas_norm', 'conversion_rate_norm', 'ctr_norm', 'engagement_rate_norm']].mean(axis=1)
platform_performance = platform_performance.sort_values('score', ascending=False)

colors_score = ['#2ecc71' if x > 60 else '#f39c12' if x > 40 else '#e74c3c' 
                for x in platform_performance['score'].values]
bars = ax12.barh(platform_performance['plataforma'], platform_performance['score'], color=colors_score)
ax12.set_xlabel('Score de Rendimiento (0-100)')
ax12.set_title('Score Integrado de Rendimiento por Plataforma')
for i, (idx, row) in enumerate(platform_performance.iterrows()):
    ax12.text(row['score'] + 2, i, f"{row['score']:.1f}", va='center')
ax12.grid(axis='x', alpha=0.3)

# 13. Análisis ROI por Tipo de Campaña
ax13.set_title('ROI Estimado por Tipo de Campaña')
roi_by_type = df.groupby('tipo_campana').agg({
    'revenue_generado': 'sum',
    'costo_total': 'sum'
}).reset_index()
roi_by_type['roi'] = ((roi_by_type['revenue_generado'] - roi_by_type['costo_total']) / roi_by_type['costo_total'] * 100)
roi_by_type = roi_by_type.sort_values('roi', ascending=False)

colors_roi = ['#2ecc71' if x > 0 else '#e74c3c' for x in roi_by_type['roi'].values]
bars = ax13.barh(roi_by_type['tipo_campana'], roi_by_type['roi'], color=colors_roi)
ax13.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
ax13.set_xlabel('ROI (%)')
ax13.set_title('Retorno sobre Inversión por Tipo de Campaña')
for i, (idx, row) in enumerate(roi_by_type.iterrows()):
    ax13.text(row['roi'] + (5 if row['roi'] > 0 else -15), i, f"{row['roi']:.1f}%", va='center')
ax13.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig('analisis_correlacion_deep.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico de correlación guardado como 'analisis_correlacion_deep.png'")

# Mostrar resumen estadístico
print("\n" + "="*60)
print("RESUMEN EJECUTIVO DEL ANÁLISIS")
print("="*60)

print("\n📊 RENDIMIENTO POR PLATAFORMA:")
platform_summary = df.groupby('plataforma').agg({
    'revenue_generado': 'sum',
    'costo_total': 'sum',
    'conversiones': 'sum',
    'roas': 'mean',
    'conversion_rate': 'mean'
}).round(2)
print(platform_summary)

print("\n📊 RENDIMIENTO POR TIPO DE CAMPAÑA:")
campaign_summary = df.groupby('tipo_campana').agg({
    'revenue_generado': 'sum',
    'costo_total': 'sum',
    'conversiones': 'sum',
    'roi': lambda x: ((df[df['tipo_campana'] == x.name]['revenue_generado'].sum() - 
                       df[df['tipo_campana'] == x.name]['costo_total'].sum()) / 
                      df[df['tipo_campana'] == x.name]['costo_total'].sum() * 100) if df[df['tipo_campana'] == x.name]['costo_total'].sum() > 0 else 0,
    'roas': 'mean'
}).round(2)
print(campaign_summary)

print("\n📊 AUDIENCIA MÁS EFECTIVA:")
audience_summary = df.groupby('audiencia_objetivo').agg({
    'conversion_rate': 'mean',
    'engagement_rate': 'mean',
    'cpc': 'mean',
    'conversiones': 'sum'
}).sort_values('conversion_rate', ascending=False).round(2)
print(audience_summary)

print("\n✓ Análisis completado exitosamente")
