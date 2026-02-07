#!/usr/bin/env python3
"""
MCP Server Tool Reference
Complete list of all tools available across MCP servers
"""

TOOLS = {
    "brave-search (port 7000)": [
        "brave_web_search - Search the web using Brave Search API",
        "brave_local_search - Search for local businesses and places",
    ],
    
    "gnomad (port 7001)": [
        "get_gene_info - Retrieve gene information from gnomAD v4",
        "search_for_genes - Search for genes in gnomAD",
        "get_region_info - Retrieve region information",
        "get_variant_info - Retrieve variant information",
        "get_clinvar_variant_info - Get ClinVar variant info",
        "get_mitochondrial_variant_info - Get mito variant info",
        "get_structural_variant_info - Get structural variant info",
        "get_copy_number_variant_info - Get CNV info",
        "search_for_variants - Search variants by ID",
        "get_str_info - Get short tandem repeat info",
        "get_variant_liftover - Get liftover info (v2)",
        "get_metadata - Get gnomAD dataset metadata",
    ],
    
    "bio-local (port 7002)": [
        "read_vcf_header - Read VCF file header",
        "query_vcf_region - Query VCF by genomic region",
        "get_variant_stats - Get variant statistics from VCF",
        "filter_vcf_by_quality - Filter VCF by quality metrics",
    ],
    
    "genome-mcp (port 7003)": [
        "query_clinvar - Query ClinVar for variant classifications",
        "get_variant_details - Get detailed variant information",
        "search_gene_variants - Search for variants by gene",
        "get_pathogenic_variants - Get pathogenic variants for a gene",
        "batch_variant_lookup - Look up multiple variants",
        "get_gene_disease_associations - Get gene-disease associations",
        "format_variant_id - Format variant ID for different databases",
        "get_variant_frequencies - Get population frequencies",
        "search_by_condition - Search variants by condition/disease",
        "get_annotation_summary - Get annotation summary for variants",
    ],
    
    "paperscraper (port 7004)": [
        "search_pubmed - Search PubMed for papers",
        "search_arxiv - Search arXiv for papers",
        "search_scholar - Search Google Scholar",
        "search_preprint_servers - Search bioRxiv/medRxiv/chemRxiv",
        "get_citations - Get citation count for a paper",
        "search_journal_impact - Search journal impact factors",
        "download_paper_pdf - Download PDF of a paper",
        "update_preprint_dumps - Update local preprint dumps",
    ],
    
    "ncbi-datasets (port 7005)": [
        "search_genomes - Search genome assemblies",
        "get_genome_info - Get genome assembly details",
        "get_genome_summary - Get genome statistics",
        "search_genes - Search genes by symbol/ID",
        "get_gene_info - Get detailed gene information",
        "get_gene_sequences - Get gene sequences",
        "search_taxonomy - Search taxonomic info",
        "get_taxonomy_info - Get taxon details",
        "get_organism_info - Get organism datasets",
        "search_assemblies - Search assemblies with filters",
        "get_assembly_info - Get assembly metadata",
        "get_assembly_reports - Get quality reports",
        "download_genome_data - Get download URLs",
        "batch_assembly_info - Batch assembly lookup",
        "search_virus_genomes - Search viral genomes",
        "get_virus_info - Get viral genome details",
        "search_proteins - Search proteins",
        "get_protein_info - Get protein details",
        "get_genome_annotation - Get annotation info",
        "search_genome_features - Search genomic features",
        "compare_genomes - Compare genome assemblies",
        "find_orthologs - Find orthologous genes",
        "get_sequence_data - Get sequence data",
        "blast_search - Perform BLAST search",
        "get_phylogenetic_tree - Get phylogenetic tree",
        "get_taxonomic_lineage - Get taxonomic lineage",
        "get_database_stats - Get database statistics",
        "search_by_bioproject - Search by BioProject",
        "search_by_biosample - Search by BioSample",
        "get_assembly_quality - Get quality metrics",
        "validate_sequences - Validate sequences",
    ],
}

def main():
    print("\n" + "=" * 70)
    print("🔧 MCP SERVER TOOL REFERENCE")
    print("=" * 70)
    
    total = 0
    for server, tools in TOOLS.items():
        print(f"\n📦 {server}")
        print("-" * 50)
        for tool in tools:
            print(f"   • {tool}")
        total += len(tools)
        print(f"   [{len(tools)} tools]")
    
    print("\n" + "=" * 70)
    print(f"📊 TOTAL: {total} tools across {len(TOOLS)} servers")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()
