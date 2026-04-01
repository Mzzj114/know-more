from django.shortcuts import render
from django.http import Http404
from .utils import get_all_docs, get_doc_content

def doc_index(request):
    """
    Renders the index page listing all available documents.
    """
    docs = get_all_docs()
    return render(request, 'docs/doc_index.html', {'docs': docs, 'nav_active': 'docs'})

def doc_detail(request, slug):
    """
    Renders a specific document based on its slug.
    """
    try:
        doc_data = get_doc_content(slug)
    except Http404 as e:
        # Pass the exception up so Django handles the 404 page naturally
        raise e
        
    context = {
        'title': doc_data['metadata'].get('title', 'Untitled'),
        'content': doc_data['html'],
        'metadata': doc_data['metadata'],
        'docs': get_all_docs(),
        'nav_active': 'docs',
    }
    
    return render(request, 'docs/doc_detail.html', context)
