import urwid

palette = {
    ("bg", 'white', 'black'),

    ("window", 'white', 'black'),
    ("window_selected", 'light red', 'black'),

    ("candidate_sha", 'brown', 'black'),
    ("candidate_sha_selected", 'black', 'brown'),

    ("candidate_date", 'light blue', 'black'),
    ("candidate_date_selected", 'light blue,bold', 'black'),

    ("candidate_committer", 'light cyan', 'black'),
    ("candidate_committer_selected", "light cyan,bold", 'black'),

    ("candidate_number_ok", 'dark green', 'black'),
    ("candidate_number_nok", 'light red', 'black'),
    ("candidate_number_selected", 'dark green,bold', 'black'),

    ("candidate_message", 'light red', 'black'),
    ("candidate_message_selected", 'black', 'light red'),

    ("scroll_line", 'light red', 'black'),
    ("scroll_line_selected", 'black,bold', 'brown'),

    ("detail_file_ok", 'light green', 'black'),
    ("detail_file_nok", 'light red', 'black'),
}
