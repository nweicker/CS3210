# def pattern_match(expression, partial=False):
# #   Evaluate input and return the name of a matching pattern (or None)
# #
# #   expression - the string that we want to compare against keywords and regex patterns
# #
# #   Partial (optional)
# #       By default, the function requires an exact match to the whole string.
# #       If 'partial' is True, it will allow a partial match from the start
# #       Partial returns the name of the pattern AND the length of the matching substring.
#
#     match = None
#     if not partial:
#     # compare the expression against each keyword
#         for word in keywords:
#             if re.match(word, expression):
#                 match = word
#                 break
#
#         # if not in keywords, compare against regex patterns
#         for pattern in regex_patterns.items():
#
#             # step into if statement if the expression exactly matches a pattern
#             if bool(re.fullmatch(pattern[1], expression)):
#
#                 # on full match, return pattern name
#                 match = pattern[0]
#                 break
#
#     if partial:
#         # check for a partial match against keywords, starting from the first character
#         for word in keywords:
#
#             # if the expression partially matches a keyword
#             match = (re.match(word, expression))
#             if match:
#                 # isolate the match name
#                 match = match.group(0).rstrip()
#
#                 # return the pattern name and length
#                 match = (match[0], len(match))
#                 break
#
#         # repeat the same process except matching against regex patterns
#         for pattern in regex_patterns.items():
#
#             # if part of the expression matches a regex pattern
#             match = (re.match(pattern, expression))
#             if match:
#                 match = match.group(0).rstrip
#                 match = pattern[0]
#
#
#         #
#         # # save the matching substring (without whitespace) as partial_match
#         # if partial_match:
#         #     partial_match = partial_match.group(0).rstrip()
#         #
#         #     # return pattern name and length of matching substring
#         #     match = (pattern[0], len(partial_match))
#
#     # if the expression doesn't fit anywhere above, there's a lexical error
#     # else:
#     #     error_message(3)
#     return match