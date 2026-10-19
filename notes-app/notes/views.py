from django.contrib import messages
from django.db import connection
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import NoteForm
from .models import Note


def note_list(request):
    q = request.GET.get("q", "").strip()
    notes = Note.objects.all()
    if q:
        notes = notes.filter(Q(title__icontains=q) | Q(content__icontains=q))
    return render(request, "notes/note_list.html", {"notes": notes, "q": q})


def note_create(request):
    form = NoteForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Note created.")
        return redirect("note_list")
    return render(request, "notes/note_form.html", {"form": form, "is_edit": False})


def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk)
    return render(request, "notes/note_detail.html", {"note": note})


def note_update(request, pk):
    note = get_object_or_404(Note, pk=pk)
    form = NoteForm(request.POST or None, instance=note)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Note updated.")
        return redirect("note_detail", pk=note.pk)
    return render(request, "notes/note_form.html", {"form": form, "is_edit": True, "note": note})


def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == "POST":
        note.delete()
        messages.success(request, "Note deleted.")
        return redirect("note_list")
    return render(request, "notes/note_confirm_delete.html", {"note": note})


@require_POST
def note_toggle_pin(request, pk):
    note = get_object_or_404(Note, pk=pk)
    note.pinned = not note.pinned
    note.save(update_fields=["pinned", "updated_at"])
    return redirect(request.POST.get("next") or "note_list")


def health(request):
    """Health check for Docker HEALTHCHECK / load balancers. Verifies DB connectivity."""
    try:
        with connection.cursor() as cur:
            cur.execute("SELECT 1")
        return JsonResponse({"status": "ok", "db": connection.vendor})
    except Exception as exc:  # noqa: BLE001
        return JsonResponse({"status": "error", "detail": str(exc)}, status=503)
