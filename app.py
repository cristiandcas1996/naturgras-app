import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Naturgras Cloud", page_icon="🐷")

st.title("🐷 Naturgras: Control de Producción")
st.markdown("---")

# 1. CONEXIÓN A GOOGLE SHEETS
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. FORMULARIO DE ENTRADA
with st.form("formulario_naturgras", clear_on_submit=False):
    st.subheader("📦 Datos de la Tanda")
    col1, col2 = st.columns(2)
    with col1:
        libras = st.number_input("Libras de empella compradas", min_value=0.0, step=0.1)
        costo_empella = st.number_input("Costo total empella (COP)", min_value=0, step=1000)
    with col2:
        otros_gastos = st.number_input("Gastos extras (Gas, pasajes, mano de obra)", min_value=0, step=500)
    
    st.divider()
    
    st.subheader("🫙 Envasado Final")
    c1, c2 = st.columns(2)
    with c1:
        n_grandes = st.number_input("Frascos GRANDES (430g) producidos", min_value=0, step=1)
        p_envase_g = st.number_input("Costo unitario envase GRANDE + tapa", min_value=0, step=100)
    with c2:
        n_pequenos = st.number_input("Frascos PEQUEÑOS (200g) producidos", min_value=0, step=1)
        p_envase_p = st.number_input("Costo unitario envase PEQUEÑO + tapa", min_value=0, step=100)

    boton_guardar = st.form_submit_button("🚀 GUARDAR Y CALCULAR", use_container_width=True)

if boton_guardar:
    # --- CÁLCULOS ---
    total_gramos = (n_grandes * 430) + (n_pequenos * 200)
    costo_envases_total = (n_grandes * p_envase_g) + (n_pequenos * p_envase_p)
    inversion_total = costo_empella + otros_gastos + costo_envases_total
    
    # Costo por gramo para asignar precio proporcional
    costo_por_gramo = inversion_total / total_gramos if total_gramos > 0 else 0
    costo_final_grande = costo_por_gramo * 430
    costo_final_pequeno = costo_por_gramo * 200
    rendimiento_real = total_gramos / libras if libras > 0 else 0
    
    # --- MOSTRAR RESULTADOS EN PANTALLA (Para tus papás) ---
    st.balloons() # ¡Efecto de celebración!
    st.success("✅ ¡Datos guardados exitosamente!")
    
    st.subheader("📊 Resumen de esta producción:")
    
    # Tarjetas visuales (Métricas)
    m1, m2, m3 = st.columns(3)
    m1.metric("Gramos Totales", f"{total_gramos}g")
    m2.metric("Rendimiento", f"{rendimiento_real:.0f} g/lb", help="El ideal es 400g")
    m3.metric("Inversión Total", f"${inversion_total:,.0f}")

    st.info(f"""
    💰 **Costos de Producción por Frasco:**
    * Cada frasco **GRANDE** costó: **${costo_final_grande:,.0f}**
    * Cada frasco **PEQUEÑO** costó: **${costo_final_pequeno:,.0f}**
    *(Sugerencia: Vende por encima de estos valores para ganar dinero)*
    """)

    # --- GUARDAR EN GOOGLE SHEETS ---
    nueva_fila = pd.DataFrame([{
        "Fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "Libras_Empella": libras,
        "Costo_Materia_Prima": costo_empella,
        "Otros_Gastos": otros_gastos,
        "Frascos_Grandes": n_grandes,
        "Frascos_Pequeños": n_pequenos,
        "Gramos_Totales": total_gramos,
        "Costo_Envases": costo_envases_total,
        "Inversion_Tanda": inversion_total,
        "Costo_Grande": round(costo_final_grande, 0),
        "Costo_Pequeño": round(costo_final_pequeno, 0)
    }])

    try:
        df_existente = conn.read()
        df_actualizado = pd.concat([df_existente, nueva_fila], ignore_index=True)
        conn.update(data=df_actualizado)
    except Exception as e:
        st.error(f"Error al enviar a la nube: {e}")

# --- SECCIÓN EXTRA: VER HISTORIAL ---
st.markdown("---")
if st.checkbox("📜 Ver historial de producciones"):
    try:
        datos_historicos = conn.read()
        st.dataframe(datos_historicos.tail(10)) # Muestra las últimas 10 filas
    except:
        st.write("Aún no hay datos en el historial.")     
st.subheader("📲 Reporte para WhatsApp")
reporte = f"""
    *Naturgras - Reporte de Producción* 🐷
    📅 Fecha: {datetime.now().strftime('%d/%m/%Y')}
    ---
    ✅ Libras: {libras} lb
    ✅ Frascos G: {n_grandes} | Frascos P: {n_pequenos}
    💰 Inversión: ${inversion_total:,.0f}
    📈 Rendimiento: {total_gramos/libras:.0f} g/lb
    ---
    💵 Costo unitario G: ${costo_final_grande:,.0f}
    💵 Costo unitario P: ${costo_final_pequeno:,.0f}
    """
st.code(reporte) # Esto les permite copiar el texto con un solo clic
