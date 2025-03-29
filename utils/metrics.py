from typing import List, Dict, Any

def calculate_help_seeker_interactivity(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculates the interactivity level of the help seeker in a thread.
    """
    help_seeker_username = data[0]['username']  # The first post is made by the Help Seeker.
    total_posts = len(data)
    
    help_seeker_posts = 0
    help_seeker_word_count = 0
    total_word_count = 0
    reply_turns = 0

    for idx, row in enumerate(data):
        post_length = len(row['post_content'].split())  # Word count of the current post
        total_word_count += post_length
        
        # Check if the post is by the help seeker
        if row['username'] == help_seeker_username:
            help_seeker_posts += 1
            help_seeker_word_count += post_length
            
            # Check if it's a reply turn (not the first post) by the help seeker
            if idx > 0 and data[idx - 1]['username'] != help_seeker_username:
                reply_turns += 1

    # Calculate metrics
    post_count_ratio = help_seeker_posts / total_posts
    avg_post_length = help_seeker_word_count / help_seeker_posts if help_seeker_posts > 0 else 0
    thread_avg_post_length = total_word_count / total_posts
    reply_turn_ratio = reply_turns / help_seeker_posts if help_seeker_posts > 0 else 0

    # Combine into a result
    interactivity_metrics = {
        "post_count_ratio": round(post_count_ratio, 2),
        "avg_post_length": round(avg_post_length, 2),
        "thread_avg_post_length": round(thread_avg_post_length, 2),
        "reply_turn_ratio": round(reply_turn_ratio, 2),
        "total_posts": total_posts,
        "help_seeker_posts": help_seeker_posts
    }
    return interactivity_metrics

def determine_turn_count(metrics: Dict[str, Any], turn_limit: int) -> int:
    """
    Determines the number of conversation turns to generate based on interactivity metrics.
    """
    
    post_count_ratio = metrics['post_count_ratio']
    reply_turn_ratio = metrics['reply_turn_ratio']
    avg_post_length = metrics['avg_post_length']

    if avg_post_length < 100:
        length_factor = 0.8
    elif avg_post_length < 140:
        length_factor = 0.9
    elif avg_post_length < 260:
        length_factor = 1
    else:
        length_factor = 1.05
    
    turn_factor = post_count_ratio * 0.4 + length_factor * 0.4 + reply_turn_ratio * 0.2
    return round_to_nearest_even(turn_factor * turn_limit)
    
def round_to_nearest_even(num: float) -> int:
    even = int(num) // 2 * 2
    return even if num - even < 1 else even + 2