import os
import frontmatter
import markdown
from django.conf import settings
from pathlib import Path
from django.http import Http404

from django.utils.translation import get_language

def get_docs_dir():
    """Returns the base directory for documentation"""
    lang = get_language() or 'zh'
    lang = lang.split('-')[0]  # e.g. 'zh-hans' -> 'zh'
    return Path(settings.BASE_DIR) / 'document' / lang

def get_all_docs():
    """Returns a list of all documents with their metadata, sorted by 'order'."""
    docs_dir = get_docs_dir()
    docs = []
    
    if not docs_dir.exists():
        return docs
        
    for file_path in docs_dir.glob('**/*.md'):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)
                metadata = post.metadata
                
                # Only include docs that have a slug
                if 'slug' in metadata:
                    docs.append({
                        'title': metadata.get('title', file_path.stem),
                        'slug': metadata.get('slug'),
                        'order': metadata.get('order', 999),
                        'file_path': file_path
                    })
        except Exception as e:
            # Silently skip files that can't be parsed
            continue
            
    # Sort docs by their order frontmatter field
    docs.sort(key=lambda x: x.get('order', 999))
    return docs

def get_doc_content(slug):
    """
    Finds a document by its slug, reads it, and converts markdown to HTML.
    Raises Http404 if not found or if path traversal is detected.
    """
    docs_dir = get_docs_dir()
    all_docs = get_all_docs()
    
    # Find the document with the matching slug
    doc_meta = next((doc for doc in all_docs if doc['slug'] == slug), None)
    
    if not doc_meta:
        raise Http404("Document not found")
        
    target = doc_meta['file_path'].resolve()
    
    # Security constraint: Ensure the resolved path is within the docs directory
    if not str(target).startswith(str(docs_dir.resolve())):
         raise Http404("Access Denied")
         
    if not target.exists() or not target.is_file():
        raise Http404("Document file is missing")
        
    try:
        with open(target, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
            
            # Convert python-markdown. Extensions can be added here later (e.g., 'fenced_code', 'codehilite')
            html_content = markdown.markdown(
                post.content,
                extensions=['extra', 'toc']
            )
            
            return {
                'metadata': post.metadata,
                'html': html_content
            }
    except Exception as e:
        raise Http404(f"Error reading document: {str(e)}")
