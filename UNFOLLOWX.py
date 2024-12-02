import os
import logging
import time
import tweepy
from typing import List, Set

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('unfollow.log'),
        logging.StreamHandler()
    ]
)

class TwitterUnfollowManager:
    def __init__(self, 
                 api_key: str, 
                 api_secret: str, 
                 access_token: str, 
                 access_secret: str):
        """
        Initialize Twitter API connection with error handling.
        
        Args:
            api_key (str): Twitter API key
            api_secret (str): Twitter API secret
            access_token (str): Twitter access token
            access_secret (str): Twitter access token secret
        """
        try:
            # Set up authentication
            auth = tweepy.OAuthHandler(api_key, api_secret)
            auth.set_access_token(access_token, access_secret)
            
            # Create API object with rate limit handling
            self.api = tweepy.API(
                auth, 
                wait_on_rate_limit=True,  # Automatically wait when rate limit is hit
                wait_on_rate_limit_notify=True  # Log when waiting
            )
            
            # Verify credentials
            self.api.verify_credentials()
            logging.info("Twitter API authentication successful.")
        except Exception as e:
            logging.error(f"Authentication failed: {e}")
            raise

    def get_followers_and_following(self) -> tuple[Set[int], Set[int]]:
        """
        Retrieve followers and following lists with comprehensive error handling.
        
        Returns:
            tuple: Sets of follower and following user IDs
        """
        try:
            followers = set(self.api.followers_ids())
            following = set(self.api.friends_ids())
            
            logging.info(f"Total followers: {len(followers)}")
            logging.info(f"Total following: {len(following)}")
            
            return followers, following
        except tweepy.TweepError as e:
            logging.error(f"Error retrieving followers/following lists: {e}")
            raise

    def unfollow_nonfollowers(
        self, 
        limit_per_minute: int = 10, 
        dry_run: bool = False
    ) -> List[int]:
        """
        Unfollow users who do not follow back.
        
        Args:
            limit_per_minute (int): Maximum number of unfollows per minute
            dry_run (bool): If True, only logs who would be unfollowed without actual unfollowing
        
        Returns:
            List of user IDs unfollowed
        """
        try:
            # Get followers and following lists
            followers, following = self.get_followers_and_following()
            
            # Identify non-followers
            nonfollowers = list(following - followers)
            
            logging.info(f"Found {len(nonfollowers)} non-followers")
            
            unfollowed_users: List[int] = []
            
            for user_id in nonfollowers:
                try:
                    # Get user details
                    user = self.api.get_user(user_id)
                    
                    if dry_run:
                        # In dry run, just log who would be unfollowed
                        logging.info(f"Would unfollow: @{user.screen_name} (ID: {user_id})")
                    else:
                        # Actually unfollow
                        self.api.destroy_friendship(user_id)
                        logging.info(f"Unfollowed: @{user.screen_name}")
                        unfollowed_users.append(user_id)
                    
                    # Rate limiting control
                    if len(unfollowed_users) >= limit_per_minute:
                        logging.info("Reached minute limit. Pausing for 60 seconds...")
                        time.sleep(60)
                
                except tweepy.TweepError as user_error:
                    logging.error(f"Error processing user {user_id}: {user_error}")
                    continue
            
            return unfollowed_users
        
        except Exception as e:
            logging.error(f"Unexpected error in unfollow process: {e}")
            return []

def main():
    """
    Main execution function with environment variable support and error handling.
    """
    try:
        # Use environment variables for sensitive information
        api_key = os.getenv('TWITTER_API_KEY')
        api_secret = os.getenv('TWITTER_API_SECRET')
        access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        access_secret = os.getenv('TWITTER_ACCESS_SECRET')
        
        # Check if all credentials are provided
        if not all([api_key, api_secret, access_token, access_secret]):
            logging.error("Missing Twitter API credentials. Set environment variables.")
            return
        
        # Initialize Twitter manager
        twitter_manager = TwitterUnfollowManager(
            api_key, api_secret, access_token, access_secret
        )
        
        # Perform unfollow (with dry run option)
        unfollowed = twitter_manager.unfollow_nonfollowers(
            limit_per_minute=10,  # Configurable
            dry_run=False  # Set to True to test without actual unfollowing
        )
        
        logging.info(f"Total users unfollowed: {len(unfollowed)}")
    
    except Exception as e:
        logging.error(f"Critical error in main execution: {e}")

if __name__ == "__main__":
    main()
