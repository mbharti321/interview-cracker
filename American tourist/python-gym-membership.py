"""
We are building a program to manage a gym's membership. The gym has multiple members, each with a unique ID, name, and membership status. The program allows gym staff to add new members, update members status, and get membership statistics.

Definitions:
* A "member" is an object that represents a gym member. It has properties for the ID, name, and membership status.
* A "membership" is a class which is used for managing members in the gym.

To begin with, we present you with two tasks:
1-1) Read through and understand the code below. Please take as much time as necessary, and feel free to run the code.
1-2) The test for Membership is not passing due to a bug in the code. Make the necessary changes to Membership to fix the bug.
"""

"""
We are currently updating our system to include information about workouts for our members. As part of this update, we have introduced the Workout class, which represents a single workout session for a member. Each object of the Workout class has a unique ID, as well as a start time and end time that are represented in the number of minutes spent from the start of the day. You can assume that all the Workouts are from the same day.

To implement these changes, we need to add two functions to the Membership class:

2.1) The `add_workout` function should be used to add a workout session for a member. If the given member does not exist while calling this function, the workout can be ignored.

2.2) The `get_average_workout_durations` function should calculate the average duration of workouts for each member in minutes and return the results as a map. 
    -> {member_id: minutes}

To assist you in testing these new functions, we have provided the test_get_average_workout_durations function.
"""

from enum import Enum
import unittest


class Workout:
    """
    This class represents a single workout session for a member.
    Each object of the Workout class has a unique ID, as well as 
    a start time and end time that are represented in the number 
    of minutes spent from the start of the day.
    """
    def __init__(self, id: int, start_time: int, end_time: int):
        self.id = id
        self.start_time = start_time
        self.end_time = end_time

    def get_duration(self):
        return self.end_time - self.start_time

class MembershipStatus(Enum):
    """
    Membership Status is of three types: BRONZE, SILVER and GOLD.
    BRONZE is the default membership a new member gets.
    SILVER and GOLD are paid memberships for the gym.
    """
    BRONZE = 1
    SILVER = 2
    GOLD = 3

class Member:
    """ Data about a gym member. """
    def __init__(self, member_id: int, name: str, membership_status: MembershipStatus):
        self.member_id = member_id
        self.name = name
        self.membership_status = membership_status
        self.workouts = []

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (
            self.member_id == other.member_id
            and self.name == other.name
            and self.membership_status == other.membership_status
        )
    
    def __str__(self):
        return f"Member ID: {self.member_id}, Name: {self.name}, Membership Status: {self.membership_status}"

class Membership:
    """
    Data for managing a gym membership, and methods which staff can
    use to perform any queries or updates.
    """
    def __init__(self):
        self.members = []

    def add_member(self, member: Member):
        """Adds a member to the gym"""
        self.members.append(member)

    def update_membership(self, member_id: int, membership_status: MembershipStatus):
        """Update membership of the given member"""
        for member in self.members:
            if member.member_id == member_id:
                member.membership_status = membership_status
                break

    def get_membership_statistics(self):
        """Calculates and returns membership statistics for all members"""
        total_members = len(self.members)
        total_paid_members = sum(1 for member in self.members if member.membership_status in  (MembershipStatus.GOLD,MembershipStatus.SILVER))
        conversion_rate = (total_paid_members / total_members) * 100
        return {
            "total_members": total_members,
            "total_paid_members": total_paid_members,
            "conversion_rate": conversion_rate
        }
        
    def add_workout(self, member_id: int, workout: Workout):
        # if(member_id not in self.members):
        #     continue
        # else:
        for member in self.members:
            if(member_id == member.member_id):
                member.workouts.append(workout)
    
    # def get_average_workout_durations
            
        

class TestSuite(unittest.TestCase):
    """ This is not a complete test suite, but tests some basic functionality of
        the code and shows how to use it.
    """
    def test_member(self):
        """Test Bronze Member functionality"""
        test_member = Member(1, "John Doe", MembershipStatus.BRONZE)
        self.assertEqual(test_member.member_id, 1)
        self.assertEqual(test_member.name, "John Doe")
        self.assertEqual(test_member.membership_status, MembershipStatus.BRONZE)

    def test_membership(self):
        """Test Bronze Membership functionality"""
        test_membership = Membership()
        test_member = Member(1, "John Doe", MembershipStatus.BRONZE)
        test_membership.add_member(test_member)
        self.assertEqual(len(test_membership.members), 1)
        self.assertEqual(test_membership.members[0], test_member)

        test_membership.update_membership(1, MembershipStatus.SILVER)
        self.assertEqual(test_membership.members[0].membership_status, MembershipStatus.SILVER)
        
        test_member_2 = Member(2, "Alex C", MembershipStatus.BRONZE)
        test_membership.add_member(test_member_2)

        test_member_3 = Member(3, "Marie C", MembershipStatus.GOLD)
        test_membership.add_member(test_member_3)

        test_member_4 = Member(4, "Joe D", MembershipStatus.SILVER)
        test_membership.add_member(test_member_4)
                
        test_member_5 = Member(5, "June R.", MembershipStatus.BRONZE)
        test_membership.add_member(test_member_5)

        attendance_stats = test_membership.get_membership_statistics()
        self.assertEqual(attendance_stats["total_members"], 5)
        self.assertEqual(attendance_stats["total_paid_members"], 3)
        self.assertAlmostEqual(attendance_stats["conversion_rate"], 60.00, 1)


    def test_get_average_workout_durations(self):
        """Test add_workout and get_average_workout_durations functions"""
        test_membership = Membership()
        test_member = Member(12, "John Doe", MembershipStatus.SILVER)
        test_membership.add_member(test_member)
        
        test_member_2 = Member(22, "Alex Cleeve", MembershipStatus.BRONZE)
        test_membership.add_member(test_member_2)

        test_member_3 = Member(31, "Marie Cardiff", MembershipStatus.GOLD)
        test_membership.add_member(test_member_3)

        test_member_4 = Member(37, "George Costanza", MembershipStatus.SILVER)
        test_membership.add_member(test_member_4)
    
        test_workout_1 = Workout(11, 10, 20)
        test_workout_2 = Workout(24, 15, 35)
        test_workout_3 = Workout(32, 45, 90)
        test_workout_4 = Workout(47, 100, 155)
        test_workout_5 = Workout(56, 120, 200)
        test_workout_6 = Workout(62, 300, 400)
        test_workout_7 = Workout(78, 1000, 1010)
        test_workout_8 = Workout(80, 1010, 1045)

        test_membership.add_workout(12, test_workout_1)
        test_membership.add_workout(22, test_workout_2)
        test_membership.add_workout(31, test_workout_3)
        test_membership.add_workout(12, test_workout_4)
        test_membership.add_workout(22, test_workout_5)
        test_membership.add_workout(31, test_workout_6)
        test_membership.add_workout(12, test_workout_7)
        test_membership.add_workout(4, test_workout_8)

        average_durations = test_membership.get_average_workout_durations()
        self.assertAlmostEqual(average_durations[12], 25.0, 1)
        self.assertAlmostEqual(average_durations[22], 50.0, 1)
        self.assertAlmostEqual(average_durations[31], 72.5, 1)
        self.assertNotIn(4, average_durations.keys())


if __name__ == "__main__":
    unittest.main()