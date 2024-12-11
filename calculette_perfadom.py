import streamlit as st
import pandas as pd

# Title of the app
st.title("Calculette PERFADOM")

# Input fields
st.header("Saisissez les informations pour chaque type de perfusion")

# Initialize session state for multiple entries
if "entries" not in st.session_state:
    st.session_state.entries = []

# User inputs for one entry
type_perfusion = st.selectbox(
    "Type de perfusion",
    ["SA", "DIFF", "GRAV"],
    key="type_perfusion"
)
nombre_perfusions = st.number_input("Nombre de perfusions par jour", min_value=1, max_value=10, step=1, key="nombre_perfusions")
type_forfait = st.selectbox(
    "Type de forfait",
    ["Installation", "Suivi", "Consommables"],
    key="type_forfait"
)

# Add entry button
if st.button("Ajouter cette entrée"):
    st.session_state.entries.append({
        "Type de perfusion": type_perfusion,
        "Nombre de perfusions": nombre_perfusions,
        "Type de forfait": type_forfait
    })
    st.success("Entrée ajoutée avec succès !")

# Display all entries
if st.session_state.entries:
    st.subheader("Entrées enregistrées")
    st.write(pd.DataFrame(st.session_state.entries))

# Tarifs
TARIFS = {
    "SA": {"Installation": 357.2, "Suivi": 164.86, "Consommables": 118.75},
    "DIFF": {"Installation": 228.97, "Suivi": 150.00, "Consommables": 100.50},
    "GRAV": {"Installation": 100.00, "Suivi": 80.00, "Consommables": 50.00}
}

# Calculate costs if inputs are valid
if st.button("Calculer les coûts totaux"):
    results = []
    for entry in st.session_state.entries:
        tarif_unitaire = TARIFS[entry["Type de perfusion"]][entry["Type de forfait"]]
        cout_total = tarif_unitaire * entry["Nombre de perfusions"]
        results.append({
            "Type de perfusion": entry["Type de perfusion"],
            "Type de forfait": entry["Type de forfait"],
            "Nombre de perfusions": entry["Nombre de perfusions"],
            "Coût unitaire (€)": tarif_unitaire,
            "Coût total (€)": cout_total
        })

    # Convert results to DataFrame
    results_df = pd.DataFrame(results)

    # Display results
    st.subheader("Résultats")
    st.write(results_df)

    # Option to download results
    st.download_button(
        label="Télécharger les résultats en Excel",
        data=results_df.to_excel(index=False, engine='openpyxl'),
        file_name="resultats_perfadom.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# Reset entries
if st.button("Réinitialiser les entrées"):
    st.session_state.entries = []
    st.success("Entrées réinitialisées avec succès !")
