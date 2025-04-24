from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver

from FlightApp.models import Pilot, Flight, FlightReport, Airline, AirlinePilot, AirlineLog


@receiver(pre_save, sender=Pilot)
def update_rank_to_pilot(sender, instance,  **kwargs):
    if instance.total_flight_hours > 1000:
        instance.rank = 'S'
    elif instance.total_flight_hours > 500:
        instance.rank = 'I'
    else:
        instance.rank = 'J'


@receiver(post_save, sender=Flight)
def generate_report_after_flight_creation(sender, instance, created, **kwargs):
    if created:
        description = f'Flight {instance.code}:\n' \
                      f'Take-off airport: {instance.take_off_airport}\n' \
                      f'Landing airport: {instance.landing_airport}\n' \
                      f'Balloon: {instance.balloon.name}\n' \
                      f'Pilot: {instance.pilot.name} {instance.pilot.surname}\n'\
                      f'Airline: {instance.airline.name}\n'

        FlightReport.objects.create(flight=instance, description=description)


@receiver(pre_delete, sender=Airline)
def assign_pilots_after_airline_deletion(sender, instance, **kwargs):
    airline_pilots = AirlinePilot.objects.filter(airline=instance).all()

    new_airline = Airline.objects.exclude(id=instance.id).first()

    for airline_pilot in airline_pilots:
        airline_pilot.airline = new_airline
        airline_pilot.save()

        # AirlinePilot.objects.create(
        #     airline=new_airline,
        #     pilot=airline_pilot.pilot
        # )


@receiver(post_delete, sender=Airline)
def log_airline_after_deletion(sender,instance, **kwargs):
    AirlineLog.objects.create(
        name=instance.name,
        year_founded=instance.year_founded,
        description=f'Airline {instance.name} is deleted from the system!'
    )