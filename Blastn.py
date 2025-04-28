import os
import subprocess

# Paths
query_folder = r"C:\Users\USER\Desktop\New_databse\Streptococcus uberis_Genomes"
blast_db = r"C:\Users\USER\Desktop\New_databse\Final_DB\Final_DB"
output_folder = r"C:\Users\USER\Desktop\New_databse\BLAST_Results-Streptococcus uberis"

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# List all FASTA files in query folder
query_files = [f for f in os.listdir(query_folder) if f.endswith(".fasta")]

# BLAST output format including aligned sequences
blast_outfmt = "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qseq sseq"

# Loop through each FASTA file and run BLAST
for query_file in query_files:
    query_path = os.path.join(query_folder, query_file)
    output_path = os.path.join(output_folder, f"{query_file.replace('.fasta', '')}_blast.txt")

    print(f"🚀 Running BLAST for {query_file}...")

    # Run BLASTn command
    blast_command = [
        "blastn",
        "-query", query_path,
        "-db", blast_db,
        "-out", output_path,
        "-outfmt", blast_outfmt,
        "-evalue", "1e-10",
        "-max_target_seqs", "10"
    ]

    # Execute the BLAST command
    subprocess.run(blast_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Check if BLAST produced results
    if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
        print(f"✅ Results saved: {output_path}")
    else:
        print(f"⚠️ No hits found for {query_file}. Skipping.")

print("🎉 BLAST analysis completed for all files!")
