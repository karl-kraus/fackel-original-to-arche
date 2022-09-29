import os
import pandas as pd
from rdflib import Graph, URIRef, Literal, Namespace, XSD
from rdflib.namespace import RDF
from config import MASTER_DF, ARCHE_BASE_ID, ARCHE_MD, OUT_DIR, ARCHE_CONSTANTS

if os.environ.get("TESTENV"):
    test_env = True
else:
    test_env = False

master_df = pd.read_csv(MASTER_DF)
ACDHNS = Namespace("https://vocabs.acdh.oeaw.ac.at/schema#")

g = Graph()
g.parse(ARCHE_CONSTANTS)

if test_env:
    master_df = master_df.head(50)

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

# constants
    g.add(
        (
            nr_col_id,
            ACDHNS.hasMetadataCreator,
            URIRef("https://id.acdh.oeaw.ac.at/acdh"),
        )
    )
    g.add((nr_col_id, ACDHNS.hasActor, URIRef('https://id.acdh.oeaw.ac.at/kkraus')))
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
    for i, row in df.iterrows():
        item_id = URIRef(f"{ARCHE_BASE_ID}/{row['f_name']}")
        g.add((item_id, RDF.type, ACDHNS.Resource))
        g.add((item_id, ACDHNS.isPartOf, nr_col_id))
        g.add(
            (
                item_id,
                ACDHNS.hasCategory,
                URIRef("https://vocabs.acdh.oeaw.ac.at/archecategory/text"),
            )
        )
        g.add(
            (
                item_id,
                ACDHNS.hasTitle,
                Literal(
                    f"Die Fackel - {df.iloc[0]['issue_title']}, Seite {row['page_nr']}", lang="de"
                ),
            )
        )
        g.add(
            (
                item_id,
                ACDHNS.hasExtent,
                Literal(
                    f"{row['word_count']} Wörter", lang="de"
                ),
            )
        )
        if len(df.iloc[0]["page_date"]) == 10:
            g.add(
                (
                    item_id,
                    ACDHNS.hasCreatedStartDateOriginal,
                    Literal(f"{df.iloc[0]['page_date']}", datatype=XSD.date),
                )
            )
            g.add(
                (
                    item_id,
                    ACDHNS.hasCreatedEndDateOriginal,
                    Literal(f"{df.iloc[0]['page_date']}", datatype=XSD.date),
                )
            )
# constants
        g.add(
            (
                item_id,
                ACDHNS.hasMetadataCreator,
                URIRef("https://id.acdh.oeaw.ac.at/acdh"),
            )
        )
        g.add((item_id, ACDHNS.hasActor, URIRef('https://id.acdh.oeaw.ac.at/kkraus')))
        g.add((item_id, ACDHNS.hasOwner, URIRef("https://id.acdh.oeaw.ac.at/acdh")))
        g.add(
            (item_id, ACDHNS.hasRightsHolder, URIRef("https://id.acdh.oeaw.ac.at/oeaw"))
        )
        g.add((item_id, ACDHNS.hasLicensor, URIRef("https://id.acdh.oeaw.ac.at/acdh")))
        g.add(
            (
                item_id,
                ACDHNS.hasLicense,
                URIRef("https://vocabs.acdh.oeaw.ac.at/archelicenses/cc-by-4-0"),
            )
        )
        g.add((item_id, ACDHNS.hasDepositor, URIRef("https://id.acdh.oeaw.ac.at/acdh")))
        g.add(
            (
                item_id,
                ACDHNS.hasLanguage,
                URIRef("https://vocabs.acdh.oeaw.ac.at/iso6393/deu"),
            )
        )


os.makedirs(OUT_DIR, exist_ok=True)
g.serialize(destination=ARCHE_MD)
