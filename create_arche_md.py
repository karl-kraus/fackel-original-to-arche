import os
import pandas as pd
from rdflib import Graph, URIRef, Literal, BNode, Namespace, XSD
from rdflib.namespace import FOAF, RDF, RDFS
from config import MASTER_DF, ARCHE_BASE_ID, ARCHE_MD, OUT_DIR

master_df = pd.read_csv(MASTER_DF)
ACDHNS = Namespace("https://vocabs.acdh.oeaw.ac.at/schema#")

g = Graph()
for i, df in master_df.groupby("nr"):
    nr_col_id = URIRef(f"{ARCHE_BASE_ID}/issue-{i}")
    g.add((nr_col_id, RDF.type, ACDHNS.Collection))
    g.add(
        (
            nr_col_id,
            ACDHNS.hasTitle,
            Literal(f"Die Fackel - {df.iloc[0]['issue_title']}", lang="de"),
        )
    )
    g.add((nr_col_id, ACDHNS.hasExtent, Literal(f"{len(df)} Seiten", lang="de")))
    g.add((nr_col_id, ACDHNS.isPartOf, URIRef(ARCHE_BASE_ID)))
    if len(df.iloc[0]["page_date"]) == 10:
        g.add(
            (
                nr_col_id,
                ACDHNS.hasCreatedStartDateOriginal,
                Literal(f"{df.iloc[0]['page_date']}", datatype=XSD.date),
            )
        )
        g.add(
            (
                nr_col_id,
                ACDHNS.hasCreatedEndDateOriginal,
                Literal(f"{df.iloc[0]['page_date']}", datatype=XSD.date),
            )
        )
    ## constants
    g.add(
        (
            nr_col_id,
            ACDHNS.hasMetadataCreator,
            URIRef("https://id.acdh.oeaw.ac.at/acdh"),
        )
    )
    g.add((nr_col_id, ACDHNS.hasOwner, URIRef("https://id.acdh.oeaw.ac.at/acdh")))
    g.add(
        (nr_col_id, ACDHNS.hasRightsHolder, URIRef("https://id.acdh.oeaw.ac.at/oeaw"))
    )
    g.add((nr_col_id, ACDHNS.hasLicensor, URIRef("https://id.acdh.oeaw.ac.at/acdh")))
    g.add(
        (
            nr_col_id,
            ACDHNS.hasLicense,
            URIRef("https://vocabs.acdh.oeaw.ac.at/archelicenses/cc-by-4-0"),
        )
    )
    g.add((nr_col_id, ACDHNS.hasDepositor, URIRef("https://id.acdh.oeaw.ac.at/acdh")))
    g.add(
        (
            nr_col_id,
            ACDHNS.hasLanguage,
            URIRef("https://vocabs.acdh.oeaw.ac.at/iso6393/deu"),
        )
    )

os.makedirs(OUT_DIR, exist_ok=True)
g.serialize(destination=ARCHE_MD)