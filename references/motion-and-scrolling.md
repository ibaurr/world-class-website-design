# Motion and Scrolling

## Default: smooth/eased scrolling

Treat smooth/eased scrolling as a default preference across website projects. The desired feel is fluid and controlled, not slow or disconnected from user input.

Before implementing:
- Inspect the framework, routing, existing animation libraries, and current scroll behavior.
- Check whether native CSS/browser behavior is sufficient.
- Add a library such as Lenis only when it offers a clear benefit.
- Avoid running multiple competing scroll controllers.

Tune the experience with real input devices. Mouse wheels, trackpads, touchscreens, keyboard navigation, and anchor links can behave differently.

## Smooth scrolling is not scroll hijacking

Smooth/eased scrolling changes the feel of movement. Scroll hijacking takes greater control of the user's scroll input. They are different techniques.

Do not globally hijack scrolling. Preserve the user's ability to move naturally through the page.

## Optional techniques

### Sticky and pinned sections
Use for a focused sequence where a visual or section remains in view while content progresses. Ensure the pin duration feels reasonable and there is a clear exit.

### Scroll-driven storytelling
Tie a visual transformation or content reveal to scroll progress. Keep the relationship between input and response understandable.

### Parallax
Use restrained layered movement to create depth. Avoid motion that harms readability or causes discomfort.

### Horizontal sequences
Use only when horizontal progression is clear and the section has a useful reason to work this way. Provide an accessible alternative on touch and reduced-motion contexts.

### Section transitions
Use transitions to establish continuity between scenes. Avoid long delays before the user can access content.

## Accessibility and resilience

- Respect `prefers-reduced-motion`.
- Keep content and navigation available when motion is disabled.
- Avoid trapping keyboard or touch users.
- Avoid scroll locks except for short, necessary UI states such as an open modal.
- Ensure focus changes and anchor navigation remain predictable.
- Avoid large layout shifts.
- Test on mobile devices and low-powered hardware when possible.

## QA checklist

- [ ] Mouse wheel feels responsive.
- [ ] Trackpad movement is not excessively damped.
- [ ] Touch scrolling remains native-feeling.
- [ ] Keyboard scrolling works.
- [ ] Anchor links reach the correct content.
- [ ] Sticky/pinned sections do not trap users.
- [ ] Route changes and dynamic content do not cause scroll jumps.
- [ ] Reduced-motion mode is usable.
- [ ] No jitter, lag, or unexpected horizontal overflow.
