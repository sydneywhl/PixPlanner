from backend.log_in_logic import has_account_been_created
from frontend.log_in import display_log_in_screen
from frontend.create_account import display_create_account_screen
from pix_utility import load_all_fonts
load_all_fonts()

if has_account_been_created():
    display_log_in_screen()
else:
    display_create_account_screen()