# Content design and interface states

Every interface state should help people understand what happened and what action is available next. Use real product terminology and avoid inventing promises, testimonials, statistics, or capabilities.

## State inventory

Before finalizing an important component or user journey, identify its normal, empty, loading, error, and successful states. Test relevant form validation and offline states too.

| State | Content requirements | Interaction requirements |
| --- | --- | --- |
| Empty | Explain why nothing appears and what useful next step exists; distinguish a first-use empty state from no search results. | Provide a clear action such as "Create project" or "Clear filters" when appropriate. |
| Loading | Set expectation using concise status text or meaningful skeletons; avoid fabricated progress percentages. | Preserve focus and context; prevent duplicate submissions; use accessible status semantics. |
| Error | Say what failed in plain language without exposing secrets, stack traces, or blaming the user. | Provide retry, correction, or recovery steps; retain entered form data where safe. |
| Success | Confirm the action with a specific outcome, not only a green icon or animation. | Offer an appropriate next action or navigation destination without unnecessary interruption. |
| Validation | Identify exactly which field needs attention and how to fix it. | Associate messages with the fields, move focus deliberately, and preserve valid input. |
| Offline / degraded | Explain what is unavailable and whether data is saved or changes will be retried, only when true. | Offer a realistic recovery path and avoid falsely claiming synchronization. |

## Meaningful microcopy

- Prefer action-specific labels ("Send invitation", "Save draft") over vague ones ("Continue", "Submit") when the destination or effect is not obvious.
- Use concise, audience-appropriate voice; avoid jargon, filler, forced enthusiasm, or manipulative urgency.
- Set realistic expectations for destructive actions, wait states, pricing, permissions, and data changes.
- Distinguish a user action from a background process. Do not say an action succeeded until there is evidence that it did.
- For accessibility, keep button names, confirmation messages, field hints, and error messages consistent with the control's behavior.
- Test text expansion and localization; microcopy in RTL languages must remain legible alongside emails, numbers, and URLs.

## Review examples

- Weak: "Oops! Something went wrong." Better: "We couldn't save your changes. Your edits are still here. Try again."
- Weak: "No data." Better: "No results match these filters. Clear filters to see all items."
- Weak: "Done!" Better: "Your invitation was sent to the selected teammate." (Only if delivery was actually confirmed.)

Never copy example claims verbatim unless they match the product's real behavior.
