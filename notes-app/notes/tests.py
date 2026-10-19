from django.test import TestCase
from django.urls import reverse

from .models import Note


class NoteTests(TestCase):
    def test_create_list_search_delete(self):
        r = self.client.post(reverse("note_create"), {"title": "Docker", "content": "multi-stage builds"})
        self.assertEqual(r.status_code, 302)
        note = Note.objects.get()

        self.assertContains(self.client.get(reverse("note_list")), "Docker")
        self.assertContains(self.client.get(reverse("note_list"), {"q": "multi-stage"}), "Docker")
        self.assertNotContains(self.client.get(reverse("note_list"), {"q": "kubernetes"}), "multi-stage")

        self.client.post(reverse("note_update", args=[note.pk]), {"title": "Docker 2", "content": "x"})
        note.refresh_from_db()
        self.assertEqual(note.title, "Docker 2")

        self.client.post(reverse("note_toggle_pin", args=[note.pk]))
        note.refresh_from_db()
        self.assertTrue(note.pinned)

        self.client.post(reverse("note_delete", args=[note.pk]))
        self.assertFalse(Note.objects.exists())

    def test_health(self):
        r = self.client.get(reverse("health"))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["status"], "ok")
