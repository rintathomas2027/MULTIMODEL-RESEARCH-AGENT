import urllib.request
import urllib.parse
import json
import xml.etree.ElementTree as ET
import re
from datetime import datetime

def resolve_arxiv_paper(query_or_id):
    """
    Fetch paper metadata from arXiv API using arXiv ID or search query.
    """
    clean_id = query_or_id.strip()
    id_match = re.search(r'(\d{4}\.\d{4,5}(?:v\d+)?)', clean_id)
    
    if id_match:
        arxiv_id = id_match.group(1)
        url = f"https://export.arxiv.org/api/query?id_list={arxiv_id}&max_results=1"
    else:
        encoded_query = urllib.parse.quote(clean_id)
        url = f"https://export.arxiv.org/api/query?search_query=all:{encoded_query}&start=0&max_results=1"

    req = urllib.request.Request(url, headers={'User-Agent': 'ScholarPulse/2.0 (mailto:scholarpulse@assistant.ai)'})
    with urllib.request.urlopen(req, timeout=10) as response:
        xml_data = response.read().decode('utf-8')

    root = ET.fromstring(xml_data)
    atom_ns = {'atom': 'http://www.w3.org/2005/Atom', 'arxiv': 'http://arxiv.org/schemas/atom'}

    entry = root.find('atom:entry', atom_ns)
    if entry is None:
        raise ValueError(f"No arXiv paper found for: {query_or_id}")

    title_elem = entry.find('atom:title', atom_ns)
    summary_elem = entry.find('atom:summary', atom_ns)
    published_elem = entry.find('atom:published', atom_ns)
    id_elem = entry.find('atom:id', atom_ns)

    authors = []
    for author in entry.findall('atom:author', atom_ns):
        name = author.find('atom:name', atom_ns)
        if name is not None and name.text:
            authors.append(name.text.strip())

    title = re.sub(r'\s+', ' ', title_elem.text.strip()) if title_elem is not None else "Untitled Paper"
    abstract = re.sub(r'\s+', ' ', summary_elem.text.strip()) if summary_elem is not None else ""
    published = published_elem.text.strip()[:10] if published_elem is not None else datetime.now().strftime('%Y-%m-%d')
    paper_id = id_elem.text.strip() if id_elem is not None else ""
    
    pdf_url = ""
    for link in entry.findall('atom:link', atom_ns):
        if link.attrib.get('title') == 'pdf' or link.attrib.get('type') == 'application/pdf':
            pdf_url = link.attrib.get('href', '')
            break
    if not pdf_url and paper_id:
        pdf_url = paper_id.replace('abs', 'pdf') + ".pdf"

    year = published[:4] if len(published) >= 4 else "2024"
    first_author_surname = authors[0].split()[-1] if authors else "ScholarPulse"
    bibtex_key = f"{first_author_surname.lower()}{year}{re.sub(r'[^a-zA-Z0-9]', '', title.split()[0].lower())}"

    bibtex = f"""@article{{{bibtex_key},
  title={{{title}}},
  author={{{' and '.join(authors)}}},
  journal={{arXiv preprint {paper_id}}},
  year={{{year}}},
  eprint={{{paper_id}}},
  archivePrefix={{arXiv}},
  primaryClass={{cs.AI}}
}}"""

    apa = f"{', '.join(authors)} ({year}). {title}. arXiv preprint {paper_id}."
    ieee = f"{', '.join(authors)}, \"{title},\" arXiv preprint {paper_id}, {year}."

    return {
        'source': 'arXiv',
        'title': title,
        'authors': authors,
        'abstract': abstract,
        'published_date': published,
        'year': year,
        'identifier': paper_id,
        'pdf_url': pdf_url,
        'bibtex': bibtex,
        'apa': apa,
        'ieee': ieee
    }

def resolve_doi_paper(doi_str):
    """
    Fetch paper metadata from CrossRef API using DOI.
    """
    clean_doi = doi_str.strip()
    clean_doi = re.sub(r'^https?://(dx\.)?doi\.org/', '', clean_doi)
    clean_doi = clean_doi.strip()

    url = f"https://api.crossref.org/works/{urllib.parse.quote(clean_doi)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'ScholarPulse/2.0 (mailto:scholarpulse@assistant.ai)'})
    
    with urllib.request.urlopen(req, timeout=10) as response:
        data = json.loads(response.read().decode('utf-8'))

    message = data.get('message', {})
    title_list = message.get('title', [])
    title = title_list[0] if title_list else "Untitled DOI Document"

    authors = []
    for a in message.get('author', []):
        given = a.get('given', '')
        family = a.get('family', '')
        if family:
            authors.append(f"{given} {family}".strip())

    published = ""
    created = message.get('created', {}).get('date-parts', [[datetime.now().year]])
    year = str(created[0][0]) if created and created[0] else str(datetime.now().year)

    publisher = message.get('publisher', 'Academic Press')
    container = message.get('container-title', ['Journal of Advanced Research'])
    journal = container[0] if container else publisher

    abstract = message.get('abstract', '')
    abstract = re.sub(r'<[^>]+>', '', abstract).strip()
    if not abstract:
        abstract = f"Abstract for {title}. Published by {publisher} in {journal} ({year})."

    first_author_surname = authors[0].split()[-1] if authors else "Author"
    bibtex_key = f"{first_author_surname.lower()}{year}{re.sub(r'[^a-zA-Z0-9]', '', title.split()[0].lower())}"

    bibtex = f"""@article{{{bibtex_key},
  title={{{title}}},
  author={{{' and '.join(authors) if authors else 'Unknown'}}},
  journal={{{journal}}},
  year={{{year}}},
  publisher={{{publisher}}},
  doi={{{clean_doi}}}
}}"""

    apa = f"{', '.join(authors) if authors else 'Author, A.'} ({year}). {title}. {journal}. https://doi.org/{clean_doi}"
    ieee = f"{', '.join(authors) if authors else 'Author, A.'}, \"{title},\" {journal}, {year}, doi: {clean_doi}."

    return {
        'source': 'CrossRef / DOI',
        'title': title,
        'authors': authors,
        'abstract': abstract,
        'published_date': year,
        'year': year,
        'identifier': clean_doi,
        'pdf_url': message.get('URL', f"https://doi.org/{clean_doi}"),
        'bibtex': bibtex,
        'apa': apa,
        'ieee': ieee
    }

def resolve_external_paper(query_or_identifier):
    """
    Smart router that detects if input is DOI, ArXiv, or general search.
    """
    text = query_or_identifier.strip()
    if 'doi.org' in text or re.match(r'^10\.\d{4,9}/[-._;()/:A-Za-z0-9]+$', text):
        try:
            return resolve_doi_paper(text)
        except Exception as e:
            print(f"DOI resolution failed: {e}, attempting fallback...")
            return resolve_arxiv_paper(text)
    else:
        return resolve_arxiv_paper(text)
