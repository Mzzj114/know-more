from django.shortcuts import render, redirect
from django.http import Http404
from .utils import get_all_docs, get_doc_content
from know_more.utils import get_language

def doc_index(request):
    """
    Renders the index page listing all available documents.
    Uses Django's i18n to detect user's language preference.
    """
    language = get_language(request)
    docs = get_all_docs(language)
    
    # If there are docs, redirect to the first one (or 'about' if exists)
    if docs:
        # Try to find 'about' doc first, otherwise use the first doc
        about_doc = next((doc for doc in docs if doc['slug'] == 'about'), None)
        target_slug = about_doc['slug'] if about_doc else docs[0]['slug']
        return redirect('doc_detail', slug=target_slug)
    
    # If no docs available, render empty index
    return render(request, 'docs/doc_index.html', {
        'docs': docs, 
        'nav_active': 'docs',
        'current_language': language
    })

def doc_detail(request, slug):
    """
    Renders a specific document based on its slug.
    Uses Django's i18n to detect user's language preference.
    """
    language = get_language(request)
    
    try:
        doc_data = get_doc_content(slug, language)
    except Http404 as e:
        # Pass the exception up so Django handles the 404 page naturally
        raise e
        
    context = {
        'title': doc_data['metadata'].get('title', 'Untitled'),
        'content': doc_data['html'],
        'metadata': doc_data['metadata'],
        'docs': get_all_docs(language),
        'nav_active': 'docs',
        'current_language': language,
    }
    
    return render(request, 'docs/doc_detail.html', context)
