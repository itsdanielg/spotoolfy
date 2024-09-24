from tqdm import tqdm
from spdu.user import get_user
from spdu.utils import extract_playlist_id, get_colored_str

sp = get_user()


def fetch_playlist_tracks(playlist_url):
    if playlist_url is None:
        return None

    playlist_id = extract_playlist_id(playlist_url)
    results = sp.playlist_tracks(playlist_id)
    tracks = results["items"]

    while results["next"]:
        results = sp.next(results)
        tracks.extend(results["items"])

    return [track["track"] for track in tracks]


def delete_playlist_tracks(playlist_url, duplicates):
    playlist_id = extract_playlist_id(playlist_url)
    track_ids = []

    # Collect track IDs from playlist 2 duplicates
    for track in duplicates:
        # Collect IDs from playlist 2 albums
        for album in track['playlist_two_albums']:
            if 'id' in album:
                track_ids.append(album['id'])

    # If there are no tracks to delete, exit the function
    if not track_ids:
        print("No tracks to delete.")
        return

    # Initialize the progress bar
    with tqdm(total=len(track_ids), desc="Deleting tracks", unit="track") as pbar:
        successful_deletions = 0
        for track_id in track_ids:
            try:
                # Attempt to remove the track
                sp.playlist_remove_all_occurrences_of_items(
                    playlist_id, [track_id])
                successful_deletions += 1
            except Exception as e:
                # Print error message in red if an exception occurs
                print(get_colored_str(
                    f"Error deleting track with ID {track_id}: {e}", "red"))
            finally:
                # Update the progress bar regardless of success or failure
                pbar.update(1)

    # Print success message in green if there were successful deletions
    if successful_deletions == 0:
        print(get_colored_str("No tracks were deleted.", "red"))
    elif successful_deletions != len(track_ids):
        print(get_colored_str(
            f"Error deleting track with ID {track_id}: {e}", "yellow"))
    else:
        print(get_colored_str(f"Successfully deleted {
            successful_deletions} tracks from the playlist.", "green"))
