Feature: User Authentication
  As a user
  I want to register and login
  So that I can create and manage blog posts

  Scenario: User registers successfully
    Given the blog application is running
    When I register with username "john_doe" and password "securepass123"
    Then the user should be created successfully
    And the password should be hashed

  Scenario: User cannot register with existing username
    Given the blog application is running
    And a user exists with username "jane_doe" and password "password123"
    When I register with username "jane_doe" and password "newpassword"
    Then the registration should fail with "Username already taken"

  Scenario: User logs in successfully
    Given the blog application is running
    And a user exists with username "testuser" and password "mypassword"
    When I login with username "testuser" and password "mypassword"
    Then a session should be created
    And I should be authenticated

  Scenario: User cannot login with wrong password
    Given the blog application is running
    And a user exists with username "testuser" and password "correctpass"
    When I login with username "testuser" and password "wrongpass"
    Then the login should fail
    And no session should be created

  Scenario: User logs out successfully
    Given the blog application is running
    And a user exists with username "logoutuser" and password "password123"
    And I am logged in as "logoutuser"
    When I logout
    Then my session should be deleted
    And I should not be authenticated
