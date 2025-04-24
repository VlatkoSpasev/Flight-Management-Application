from django.test import TestCase

from FlightApp.models import Pilot, Flight, Airline, Balloon, FlightReport, AirlinePilot


# Create your tests here.


class FlightManagementTestCase(TestCase):
    def setUp(self):
        self.pilot1 = Pilot.objects.create(name='John', surname='Doe', total_flight_hours=300, rank='S', year_of_birth=2001)
        self.pilot2 = Pilot.objects.create(name='Jane', surname='Doe', total_flight_hours=800, rank='S', year_of_birth=2001)
        self.pilot3 = Pilot.objects.create(name='Ben', surname='Doe', total_flight_hours=1200, rank='S', year_of_birth=2001)
        self.airline1 = Airline.objects.create(name='TestAirline', year_founded=2007, outside_Europe=True)
        self.airline2 = Airline.objects.create(name='MacedoniaAirline', year_founded=2001, outside_Europe=True)
        self.balloon = Balloon.objects.create(name='SmallBallon', type='S', manufacturer='TestManufacturer', max_passengers=10)

    def test_pre_save_signal_pilot_update_rank(self):
        self.pilot1.total_flight_hours = 250
        self.pilot1.save()

        self.assertEqual(self.pilot1.rank, 'J')

        self.pilot1.total_flight_hours = 700
        self.pilot1.save()

        self.assertEqual(self.pilot1.rank, 'I')

        self.pilot1.total_flight_hours = 1500
        self.pilot1.save()

        self.assertEqual(self.pilot1.rank, 'S')

    def test_generate_report_after_flight_creation(self):
        flight = Flight.objects.create(
            code='456789',
            pilot=self.pilot1,
            airline=self.airline1,
            balloon=self.balloon,
        )

        report_exists = FlightReport.objects.filter(flight=flight).exists()

        # self.assertTrue(report_exists)
        self.assertEqual(report_exists, True)

    def test_assign_pilots_after_airline_deletion(self):
        AirlinePilot.objects.create(airline=self.airline1,pilot=self.pilot1)
        AirlinePilot.objects.create(airline=self.airline1,pilot=self.pilot2)
        AirlinePilot.objects.create(airline=self.airline1,pilot=self.pilot3)

        self.airline1.delete()


        pilots_count = AirlinePilot.objects.filter(airline=self.airline2).count()

        self.assertEqual(pilots_count, 3)





