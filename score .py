import pandas as pd
import re

# === STEP 1: Load the Excel file ===
file_path = r"C:\Users\USER\Downloads\april18\april18\Combined.xlsx"
df = pd.read_excel(file_path)

# === STEP 2: Clean column headers ===
df.columns = df.columns.str.strip().str.replace(' ', '_').str.lower()

# === STEP 2A: Normalize functional_category column ===
def normalize_category(cat):
    return re.sub(r'[^a-z0-9]+', '_', cat.strip().lower())

df['functional_category'] = df['functional_category'].astype(str).apply(normalize_category)

# Print to verify all cleaned functional categories
print("🧬 Unique functional categories (cleaned):")
print(sorted(df['functional_category'].unique()))

# === STEP 2B: Define gene groups with normalized names ===
virulence_genes = {
    "adherence", "biofilm", "motility", "invasion", "exoenzyme",
    "exotoxin", "effector_delivery_system", "regulation", "stress_survival",
    "antimicrobial_activity_competitive_advantage", "immune_modulation",
    "nutritional_metabolic_factor", "metal_ion_transport", "post_translational_modification"
}

core_virulence_genes = {"exotoxin", "effector_delivery_system", "invasion"}

resistance_genes = {
    "aminoglycoside_resistance_genes", "oxazolidinone_and_phenicol_resistance_genes",
    "fosfomycin_resistance_genes", "trimethoprim_resistance_genes", "chloramphenicol_resistance_genes",
    "phenicol_resistance_genes", "macrolide_resistance_genes", "tetracycline_resistance_genes",
    "fluoroquinolone_resistance_genes", "rifamycin_resistance_genes", "carbapenem_resistance_genes",
    "colistin_polymyxin_resistance_genes", "methicillin_beta_lactams_resistance_genes",
    "multidrug_resistance_efflux_pump", "streptogramin_a_resistance_genes",
    "vancomycin_resistance_genes", "sulfonamide_resistance_genes", "nitroimidazole_resistance_genes",
    "fusidic_acid_resistance_genes", "oleandomycin_resistance_genes", "quaternary_ammonium_compound_resistance_genes",
    "beta_lactam_resistance_genes"
}

mobile_elements = {"ice", "ime", "other_mobile_elements"}

# === STEP 3: Create Presence Matrix ===
rf_matrix = df.drop_duplicates().assign(present=1)
rf_matrix = rf_matrix.pivot_table(index='genome_id',
                                  columns='functional_category',
                                  values='present',
                                  fill_value=0).reset_index()

# === STEP 4: Classification Functions ===

def classify(row):
    present_genes = {col for col in row.index if row[col] == 1}

    vir_hits = virulence_genes & present_genes
    res_hits = resistance_genes & present_genes
    mob_hits = mobile_elements & present_genes
    core_hits = core_virulence_genes & present_genes

    virulence_count = len(vir_hits)
    core_virulence_count = len(core_hits)

    # If 2 or more core virulence genes are present
    if core_virulence_count >= 2:
        virulence_status = "Dangerously Virulent"
    # If 1 core virulence gene is present and at least 1 non-core virulence gene
    elif core_virulence_count == 1 and len(vir_hits - core_virulence_genes) >= 1:
        virulence_status = "Dangerously Virulent"
    # If 5 or more virulence genes
    elif virulence_count >= 5:
        virulence_status = "Dangerously Virulent"
        
           # If 1 core virulence gene is present and no other virulence genes are found
    elif core_virulence_count == 1 and virulence_count == 1:
        virulence_status = "Strong Virulence"
        
    # If 3-4 virulence genes
    elif virulence_count >= 3:
        virulence_status = "Strong Virulence"
    # If 1-2 virulence genes
    elif virulence_count >= 1:
        virulence_status = "Early Sign of Virulence"
    else:
        virulence_status = "No Virulence Detected"

    # Resistance scoring
    resistance_count = len(res_hits)
    if resistance_count >= 3:
        resistance_status = "Dangerously Resistant"
    elif resistance_count == 2:
        resistance_status = "Strong Resistance"
    elif resistance_count == 1:
        resistance_status = "Early Resistance Detected"
    else:
        resistance_status = "No Resistance Detected"

    # Mobile elements scoring
    if "ice" in mob_hits:
        mobile_status = "Potential Horizontal Gene Transfer"
    elif mob_hits:
        mobile_status = "Genomic Instability"
    else:
        mobile_status = "Stable Genome"

    return pd.Series([
        virulence_status, virulence_count,
        resistance_status, resistance_count,
        mobile_status
    ])

# Apply classification
rf_matrix[['Virulence_Status', 'Virulence_Gene_Count',
           'Resistance_Status', 'Resistance_Gene_Count',
           'Mobile_Element_Status']] = rf_matrix.apply(classify, axis=1)



# === STEP 5: Load classification rules ===
classification_rules = []
with open(r"C:\Users\USER\Downloads\Classification.txt", "r") as f:
    headers = f.readline().strip().split("\t")
    for line in f:
        parts = line.strip().split("\t")
        if len(parts) == 4:
            classification_rules.append({
                "Virulence": parts[0],
                "Resistance": parts[1],
                "Mobile_Element": parts[2],
                "Classification": parts[3]
            })

rules_df = pd.DataFrame(classification_rules)

# === STEP 6: Final Classification Logic ===
def final_classification(row):
    vir = row['Virulence_Status']
    res = row['Resistance_Status']
    mob = row['Mobile_Element_Status']
    
    match = rules_df[
        (rules_df['Virulence'] == vir) &
        (rules_df['Resistance'] == res) &
        (rules_df['Mobile_Element'] == mob)
    ]
    if not match.empty:
        return match.iloc[0]['Classification']
    
    match = rules_df[
        (rules_df['Virulence'] == vir) &
        (rules_df['Resistance'] == res) &
        (rules_df['Mobile_Element'] == "Any")
    ]
    if not match.empty:
        return match.iloc[0]['Classification']

    if vir != "No Virulence Detected" and res != "No Resistance Detected":
        return f"Combined Threat: {vir} and {res}"
    elif vir != "No Virulence Detected":
        return f"Virulence Threat: {vir}"
    elif res != "No Resistance Detected":
        return f"Resistance Threat: {res}"
    else:
        return "Low Risk Bacterial Strain"

# Apply final classification
rf_matrix["Final_Classification"] = rf_matrix.apply(final_classification, axis=1)

# === STEP 7: Save Output ===
output_path = r"C:\Users\USER\Downloads\april18\april18\Matrix-PS.csv"
rf_matrix.to_csv(output_path, index=False)

print("✔️ Full matrix with classifications saved to:\n", output_path)
