import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración visual
st.set_page_config(page_title="Naturgras App", page_icon="🐷")

st.title("🐷 Naturgras: Calculadora de Producción")
st.markdown("---")

# 1. ENTRADA DE DATOS
with st.form("formulario_naturgras"):
    st.subheader("📦 Inversión de la Tanda")
    
    col1, col2 = st.columns(2)
    with col1:
        libras = st.number_input("Libras de empella (lb)", min_value=0.1, value=1.0, step=0.1)
        costo_empella = st.number_input("Costo total empella ($)", min_value=0, step=1000)
    with col2:
        otros_gastos = st.number_input("Otros gastos (Gas, pasajes, etc) ($)", min_value=0, step=500)
    
    st.divider()
    
    st.subheader("🫙 Envasado (Producción Final)")
    c1, c2 = st.columns(2)
    with c1:
        n_grandes = st.number_input("Frascos GRANDES (430g)", min_value=0, step=1)
        p_envase_g = st.number_input("Costo envase GRANDE unitario ($)", min_value=0, step=100)
    with c2:
        n_pequenos = st.number_input("Frascos PEQUEÑOS (200g)", min_value=0, step=1)
        p_envase_p = st.number_input("Costo envase PEQUEÑO unitario ($)", min_value=0, step=100)

    boton_calcular = st.form_submit_button("🚀 CALCULAR AHORA", use_container_width=True)

# 2. LÓGICA DE CÁLCULO
if boton_calcular:
    # Cálculos de masa y costos
    total_gramos = (n_grandes * 430) + (n_pequenos * 200)
    costo_envases_total = (n_grandes * p_envase_g) + (n_pequenos * p_envase_p)
    inversion_total = costo_empella + otros_gastos + costo_envases_total
    
    # Rendimiento
    rendimiento = total_gramos / libras if libras > 0 else 0
    
    # Costos por frasco (Proporcional al peso)
    costo_por_gramo = inversion_total / total_gramos if total_gramos > 0 else 0
    costo_final_grande = costo_por_gramo * 430
    costo_final_pequeno = costo_por_gramo * 200

    # --- RESULTADOS EN PANTALLA ---
    st.balloons()
    st.success("✨ ¡Cálculos completados!")

    # Métricas principales
    m1, m2, m3 = st.columns(3)
    m1.metric("Gramos Totales", f"{total_gramos}g")
    m2.metric("Rendimiento", f"{rendimiento:.0f} g/lb")
    m3.metric("Inversión Total", f"${inversion_total:,.0f}")

    # Cuadro de costos finales
    st.info(f"""
    ### 💰 Costo de fabricación:
    * **Frasco GRANDE (430g):** ${costo_final_grande:,.0f}
    * **Frasco PEQUEÑO (200g):** ${costo_final_pequeno:,.0f}
    """)

    # --- REPORTE PARA COPIAR ---
    st.subheader("📲 Reporte para WhatsApp")
    reporte_texto = f"""*Naturgras - Reporte de Producción* 🐷
📅 Fecha: {datetime.now().strftime('%d/%m/%Y')}
---
✅ Libras: {libras} lb
✅ Frascos G: {n_grandes} | Frascos P: {n_pequenos}
💰 Inversión Total: ${inversion_total:,.0f}
📈 Rendimiento: {rendimiento:.0f} g/lb
---
💵 Costo unitario G: ${costo_final_grande:,.0f}
💵 Costo unitario P: ${costo_final_pequeno:,.0f}"""
    
    st.text_area("Copia este texto y pégalo en el chat de la empresa:", value=reporte_texto, height=200)
    st.caption("Mantén presionado el texto para copiarlo en tu celular.")
