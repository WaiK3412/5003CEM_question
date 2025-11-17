# QUESTION 2.1: Unweighted Directed Graph Data Structure
class Graph:
    def __init__(self):
        # Dictionary to store vertex data: {vertex_id: vertex_data_object}
        self.vertices = {}

        # Dictionary to store edges: {vertex_id: [list of vertices it connects to]}
        # This represents OUTGOING edges (who this vertex follows)
        self.edges = {}

    def add_vertex(self, vertex_id, vertex_data):
        # Only add if vertex doesn't already exist
        if vertex_id not in self.vertices:
            self.vertices[vertex_id] = vertex_data
            self.edges[vertex_id] = []  # Initialize empty edge list
            return True
        return False

    def add_edge(self, from_vertex, to_vertex):
        # Create a directed edge from one vertex to another
        # Both vertices must exist first
        if from_vertex in self.vertices and to_vertex in self.vertices:
            # Avoid duplicate edges
            if to_vertex not in self.edges[from_vertex]:
                self.edges[from_vertex].append(to_vertex)
                return True
        return False

    def remove_edge(self, from_vertex, to_vertex):
        # Remove a directed edge between two vertices
        if from_vertex in self.vertices and to_vertex in self.edges[from_vertex]:
            self.edges[from_vertex].remove(to_vertex)
            return True
        return False

    def list_outgoing_adjacent_vertices(self, vertex_id):
        # Return list of vertices this vertex connects TO
        # (people this user follows)
        if vertex_id in self.edges:
            return self.edges[vertex_id]
        return []

    def list_incoming_adjacent_vertices(self, vertex_id):
        # Return list of vertices that connect TO this vertex
        # (people who follow this user)
        incoming = []

        # Check every vertex in the graph
        for vertex, adjacent_list in self.edges.items():
            # If this vertex appears in another vertex's edge list,
            # it means that vertex has an edge pointing TO this one
            if vertex_id in adjacent_list:
                incoming.append(vertex)

        return incoming

    def get_vertex_data(self, vertex_id):
        # Retrieve the data object associated with a vertex
        return self.vertices.get(vertex_id, None)

    def get_all_vertices(self):
        # Get list of all vertex IDs in the graph
        return list(self.vertices.keys())


# QUESTION 2.2: Person Entity Class
class Person:
    def __init__(self, name, gender, biography, privacy="public"):
        self.name = name
        self.gender = gender
        self.biography = biography
        self.privacy = privacy  # Can be "public" or "private"

    def display_profile(self):
        # Show profile information based on privacy settings
        if self.privacy == "private":
            return f"Name: {self.name} [PRIVATE PROFILE]"
        else:
            return f"Name: {self.name}\nGender: {self.gender}\nBio: {self.biography}\nPrivacy: {self.privacy}"

    def __str__(self):
        return self.name


# QUESTION 2.3 & 2.4: Social Media Application
class SocialMediaApp:
    def __init__(self):
        self.graph = Graph()
        self.initialize_profiles()

    def initialize_profiles(self):
        # Create initial user profiles (5-10 users as required)
        profiles = [
            Person("Alice", "Female", "Coffee lover and book enthusiast", "public"),
            Person("Bob", "Male", "Fitness trainer and health advocate", "public"),
            Person("Charlie", "Male", "Software developer passionate about AI", "private"),
            Person("Diana", "Female", "Travel blogger exploring the world", "public"),
            Person("Eve", "Female", "Artist and creative soul", "private"),
            Person("Frank", "Male", "Foodie and amateur chef", "public"),
            Person("Grace", "Female", "Marketing professional", "public"),
        ]

        print("\n" + "=" * 70)
        print("INITIALIZING USER PROFILES...")
        print("=" * 70)

        # Add each person as a vertex in the graph
        for person in profiles:
            self.graph.add_vertex(person.name, person)
            print(f"✓ Created profile: {person.name}")

        # Create initial follow relationships (directed edges)
        follow_relationships = [
            ("Alice", "Bob"),
            ("Alice", "Diana"),
            ("Bob", "Alice"),
            ("Bob", "Frank"),
            ("Charlie", "Alice"),
            ("Charlie", "Grace"),
            ("Diana", "Alice"),
            ("Diana", "Grace"),
            ("Eve", "Charlie"),
            ("Eve", "Diana"),
            ("Frank", "Bob"),
            ("Frank", "Grace"),
            ("Grace", "Diana"),
            ("Grace", "Frank"),
        ]

        print("\n" + "=" * 70)
        print("CREATING FOLLOW CONNECTIONS...")
        print("=" * 70)

        # Add each relationship as a directed edge
        for follower, following in follow_relationships:
            self.graph.add_edge(follower, following)
            print(f"✓ {follower} is now following {following}")

        print(f"\n✓ Successfully initialized {len(profiles)} profiles!")

    # ===================================================================
    # MANDATORY FEATURES (a-d)
    # ===================================================================

    def display_all_users(self):
        # MANDATORY (a): Display list of all users
        print("\n" + "=" * 70)
        print("ALL USERS")
        print("=" * 70)

        users = self.graph.get_all_vertices()
        for i, user in enumerate(users, 1):
            print(f"{i}.) {user}")

        print("=" * 70)

    def view_profile(self):
        # MANDATORY (b): View detailed profile of a user
        print("\n" + "=" * 70)
        print("VIEW USER PROFILE")
        print("=" * 70)

        self.display_all_users()

        user_name = input("\nEnter the name of user to view: ")
        person = self.graph.get_vertex_data(user_name)

        if person:
            print("\n" + "-" * 70)
            print(person.display_profile())
            print("-" * 70)
        else:
            print(f"\n✗ User '{user_name}' not found!")

    def view_following_list(self):
        # MANDATORY (c): View list of accounts a user follows
        print("\n" + "=" * 70)
        print("VIEW FOLLOWING LIST")
        print("=" * 70)

        self.display_all_users()

        user_name = input("\nEnter the name of user: ")

        # Check if user exists
        if user_name not in self.graph.vertices:
            print(f"\n✗ User '{user_name}' not found!")
            return

        # Get outgoing edges (people this user follows)
        following_list = self.graph.list_outgoing_adjacent_vertices(user_name)

        print(f"\n--- {user_name}'s Following List ---")
        if following_list:
            for i, followed_user in enumerate(following_list, 1):
                print(f"{i}.) {followed_user}")
            print(f"\nTotal: {len(following_list)} accounts")
        else:
            print(f"{user_name} is not following anyone.")
        print("-" * 70)

    def view_followers_list(self):
        # MANDATORY (d): View list of a user's followers
        print("\n" + "=" * 70)
        print("VIEW FOLLOWERS LIST")
        print("=" * 70)

        self.display_all_users()

        user_name = input("\nEnter the name of user: ")

        # Check if user exists
        if user_name not in self.graph.vertices:
            print(f"\n✗ User '{user_name}' not found!")
            return

        # Get incoming edges (people who follow this user)
        followers_list = self.graph.list_incoming_adjacent_vertices(user_name)

        print(f"\n--- {user_name}'s Followers ---")
        if followers_list:
            for i, follower in enumerate(followers_list, 1):
                print(f"{i}.) {follower}")
            print(f"\nTotal: {len(followers_list)} followers")
        else:
            print(f"{user_name} has no followers.")
        print("-" * 70)

    # ===================================================================
    # ADVANCED FEATURES (a-d)
    # ===================================================================

    def add_user_profile(self):
        # ADVANCED (a): Add new user profile on-demand
        print("\n" + "=" * 70)
        print("ADD NEW USER PROFILE")
        print("=" * 70)

        name = input("Enter name: ")

        # Check for duplicate names
        if name in self.graph.vertices:
            print(f"\n✗ User '{name}' already exists!")
            return

        gender = input("Enter gender: ")
        biography = input("Enter biography: ")
        privacy = input("Privacy setting (public/private): ").lower()

        # Validate privacy input
        if privacy not in ["public", "private"]:
            privacy = "public"

        # Create new person object and add to graph
        new_person = Person(name, gender, biography, privacy)
        self.graph.add_vertex(name, new_person)

        print(f"\n✓ Successfully created profile for {name}!")

    def follow_user(self):
        # ADVANCED (c): Allow user X to follow user Y on-demand
        print("\n" + "=" * 70)
        print("FOLLOW A USER")
        print("=" * 70)

        self.display_all_users()

        # Get the follower (person who wants to follow)
        follower = input("\nWho wants to follow someone? Enter name: ")

        # Validate follower exists
        if follower not in self.graph.vertices:
            print(f"\n✗ User '{follower}' not found!")
            return

        # Get the person to follow
        to_follow = input(f"Who should {follower} follow? Enter name: ")

        # Validate user to follow exists
        if to_follow not in self.graph.vertices:
            print(f"\n✗ User '{to_follow}' not found!")
            return

        # Can't follow yourself
        if follower == to_follow:
            print(f"\n✗ You cannot follow yourself!")
            return

        # Check if already following
        current_following = self.graph.list_outgoing_adjacent_vertices(follower)
        if to_follow in current_following:
            print(f"\n✗ {follower} is already following {to_follow}!")
            return

        # Create the follow relationship (directed edge)
        success = self.graph.add_edge(follower, to_follow)

        if success:
            print(f"\n✓ Success! {follower} is now following {to_follow}")
        else:
            print(f"\n✗ Failed to create follow relationship")

    def unfollow_user(self):
        # ADVANCED (d): Allow user X to unfollow user Y on-demand
        print("\n" + "=" * 70)
        print("UNFOLLOW A USER")
        print("=" * 70)

        self.display_all_users()

        # Get the unfollower
        unfollower = input("\nWho wants to unfollow someone? Enter name: ")

        # Validate unfollower exists
        if unfollower not in self.graph.vertices:
            print(f"\n✗ User '{unfollower}' not found!")
            return

        # Show who they're currently following
        current_following = self.graph.list_outgoing_adjacent_vertices(unfollower)

        if not current_following:
            print(f"\n✗ {unfollower} is not following anyone!")
            return

        print(f"\n{unfollower} is currently following:")
        for i, user in enumerate(current_following, 1):
            print(f"{i}.) {user}")

        # Get the person to unfollow
        to_unfollow = input(f"\nWho should {unfollower} unfollow? Enter name: ")

        # Validate they're actually following this person
        if to_unfollow not in current_following:
            print(f"\n✗ {unfollower} is not following {to_unfollow}!")
            return

        # Remove the follow relationship (directed edge)
        success = self.graph.remove_edge(unfollower, to_unfollow)

        if success:
            print(f"\n✓ Success! {unfollower} has unfollowed {to_unfollow}")
        else:
            print(f"\n✗ Failed to remove follow relationship")

    def run(self):
        # Main menu loop
        while True:
            print("\n" + "=" * 70)
            print("SLOWGRAM - YOUR SOCIAL MEDIA APP")
            print("=" * 70)
            print("1. View names of all profiles")
            print("2. View details for any profiles")
            print("3. View followers of any profile")
            print("4. View followed accounts of any profile")
            print("5. Add a new user profile")
            print("6. Follow a user")  
            print("7. Unfollow a user")  
            print("8. Quit")
            print("=" * 70)

            choice = input("Enter your choice (1-8): ")

            if choice == "1":
                self.display_all_users()
            elif choice == "2":
                self.view_profile()
            elif choice == "3":
                self.view_followers_list()
            elif choice == "4":
                self.view_following_list()
            elif choice == "5":
                self.add_user_profile()
            elif choice == "6":
                self.follow_user()  
            elif choice == "7":
                self.unfollow_user() 
            elif choice == "8":
                print("\n✓ Thank you for using Slowgram!")
                break
            else:
                print("\n✗ Invalid choice! Please try again.")


# Main execution
if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("QUESTION 2: GRAPH DATA STRUCTURE")
    print("=" * 70)

    app = SocialMediaApp()
    app.run()
