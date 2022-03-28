from django.db.models.signals import post_save
from django.dispatch import receiver
from VocabularyManagement.models import StudySet
from .models import Document


###not working right now
@receiver(post_save, sender=Document)
def create_studySet(sender, instance, created, **kwargs):
    print("signal function")
    if created:
        print(instance)
        print(sender)
        StudySet.objects.create(owner_id=instance.owner_id, generated_by=instance, title=instance.filename)
