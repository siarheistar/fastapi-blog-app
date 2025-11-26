Feature: Blog Post Management
  As an authenticated user
  I want to create and view blog posts
  So that I can share my thoughts

  Scenario: Authenticated user creates a blog post
    Given the blog application is running
    And a user exists with username "blogger" and password "blogpass"
    And I am logged in as "blogger"
    When I create a post with title "My First Post" and content "This is my first blog post"
    Then the post should be created successfully
    And the post should appear in the recent posts list

  Scenario: Create blog post with image
    Given the blog application is running
    And a user exists with username "photographer" and password "photopass"
    And I am logged in as "photographer"
    When I create a post with title "Photo Blog" and content "Check out this photo" and an image
    Then the post should be created successfully
    And the post should have an image attached

  Scenario: Unauthenticated user cannot create posts
    Given the blog application is running
    When I try to create a post without authentication
    Then the post creation should be rejected

  Scenario: View all blog posts
    Given the blog application is running
    And there are 5 existing blog posts
    When I visit the homepage
    Then I should see all 5 posts

  Scenario: View individual blog post
    Given the blog application is running
    And a post exists with id 1 and title "Test Post"
    When I view post with id 1
    Then I should see the post title "Test Post"
    And I should see the post content

  Scenario: View non-existent post redirects to homepage
    Given the blog application is running
    When I try to view post with id 9999
    Then I should be redirected to the homepage
