# Feature Specification: URL Shortener with Click Stats

**Feature Branch:** `001-url-shortener`
**Status:** Draft → Reviewed
**Input:** Build a URL shortener web service. Users can submit a long URL via a form and receive a short code. Visiting the short URL redirects to the original and increments a click counter. A stats page shows the original URL, click count and creation date for any code. Recent shortened URLs are listed on the home page. Single-user, no auth, no expiry.

---

## User Scenarios & Testing

### Primary User Story
As a single user, I want to paste a long URL, get a short code back, share that short URL, and later see how often it has been clicked.

### Acceptance Scenarios

1. **Shorten a URL**
   - **Given** the home page is open
   - **When** I paste `https://example.com/very/long/path?q=1` into the form and submit
   - **Then** a short code (6 alphanumeric chars) is displayed, along with the full short URL `http://localhost:8000/{code}`
   - **And** the new entry appears in the "Recent URLs" table on the home page

2. **Follow a short URL**
   - **Given** a short code `abc123` exists for `https://example.com`
   - **When** I visit `http://localhost:8000/abc123`
   - **Then** I am redirected (HTTP 307) to `https://example.com`
   - **And** the click count for `abc123` is incremented by 1

3. **View stats for a code**
   - **Given** code `abc123` has been clicked 5 times
   - **When** I visit `http://localhost:8000/stats/abc123`
   - **Then** I see the original URL, the count `5`, and the creation date

4. **Stats for unknown code**
   - **Given** code `nope42` does not exist
   - **When** I visit `http://localhost:8000/stats/nope42`
   - **Then** I get an HTTP 404 with a friendly message

### Edge Cases
- Submitting an invalid URL (no scheme) → 400 with error displayed on the form
- Submitting the same URL twice → produces two separate codes (de-dup is out of scope)
- Code collision on insert (unlikely but possible) → retry up to 5 times, then 500

## Functional Requirements

- **FR-001:** System MUST accept a long URL via `POST /shorten` and return a short code
- **FR-002:** Short codes MUST be 6 alphanumeric characters (case-sensitive)
- **FR-003:** System MUST redirect from `GET /{code}` to the stored original URL with HTTP 307
- **FR-004:** Each redirect MUST atomically increment the click counter for that code
- **FR-005:** System MUST expose `GET /stats/{code}` returning original URL, click count, creation timestamp
- **FR-006:** Home page `GET /` MUST display a shorten-form and a table of the 10 most recent codes with counts
- **FR-007:** System MUST validate that submitted URLs start with `http://` or `https://`
- **FR-008:** System MUST persist data across restarts (SQLite file `shortly.db`)

## Key Entities

- **ShortURL**
  - `code` (str, 6 chars, PK)
  - `url` (str, the long URL)
  - `clicks` (int, default 0)
  - `created_at` (ISO timestamp)

## Out of Scope

- Authentication, user accounts
- Custom slugs chosen by the user
- URL expiration / TTL
- Click analytics over time (only a single integer counter)
- Rate limiting
- API keys
- Public deployment concerns (HTTPS, domain config)

## Success Criteria

- A new user can shorten a URL and follow the short link in under 30 seconds
- All click counts are consistent under sequential access (no concurrency requirements for v1)
- `pytest` suite covers all 4 acceptance scenarios
