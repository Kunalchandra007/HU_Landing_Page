# Admin Panel Guide

## Overview
The admin panel is now fully integrated with the Events and Happenings sections on the main website. All content can be managed through the admin dashboard without any hardcoding.

## Features Implemented

### 1. Admin Login
- **URL**: `/admin/login`
- **Credentials**:
  - Username: `admin`
  - Password: `admin123`
- Uses localStorage for session management
- Automatic redirect if already logged in

### 2. Admin Dashboard
- **URL**: `/admin/dashboard`
- Displays all events and happenings from database
- Shows event/happening cards with:
  - Image
  - Title
  - Description (truncated to 100 chars)
  - Date (for events)
  - Delete button

### 3. Add Event
- **URL**: `/admin/events/add`
- **Form Fields**:
  - Event Title (required)
  - Event Description (required)
  - Event Date (required)
  - Event Image (required - png, jpg, jpeg, gif, webp, avif)
- **Features**:
  - Image preview before upload
  - Form validation
  - Success/error messages
  - Auto-redirect to dashboard after success

### 4. Add Happening
- **URL**: `/admin/happenings/add`
- **Form Fields**:
  - Happening Title (required)
  - Happening Description (required)
  - Happening Image (required - png, jpg, jpeg, gif, webp, avif)
- **Features**:
  - Image preview before upload
  - Form validation
  - Success/error messages
  - Auto-redirect to dashboard after success

### 5. Delete Functionality
- Delete button on each event/happening card
- Confirmation dialog before deletion
- Automatically removes image file from server
- Refreshes dashboard after deletion

### 6. Edit Event
- **URL**: `/admin/events/edit/:id`
- **Form Fields**:
  - Event Title (pre-filled)
  - Event Description (pre-filled)
  - Event Date (pre-filled)
  - Event Image (optional - shows current image, can upload new one)
- **Features**:
  - Loads existing event data
  - Shows current image
  - Optional image replacement
  - Form validation
  - Success/error messages
  - Auto-redirect to dashboard after success

### 7. Edit Happening
- **URL**: `/admin/happenings/edit/:id`
- **Form Fields**:
  - Happening Title (pre-filled)
  - Happening Description (pre-filled)
  - Happening Image (optional - shows current image, can upload new one)
- **Features**:
  - Loads existing happening data
  - Shows current image
  - Optional image replacement
  - Form validation
  - Success/error messages
  - Auto-redirect to dashboard after success

## Backend API Endpoints

### Events
- `GET /api/events` - Get all active events
- `GET /api/admin/events/:id` - Get single event by ID
- `POST /api/admin/events` - Create new event (multipart/form-data)
- `PUT /api/admin/events/:id` - Update event by ID (multipart/form-data)
- `DELETE /api/admin/events/:id` - Delete event by ID

### Happenings
- `GET /api/happenings` - Get all active happenings
- `GET /api/admin/happenings/:id` - Get single happening by ID
- `POST /api/admin/happenings` - Create new happening (multipart/form-data)
- `PUT /api/admin/happenings/:id` - Update happening by ID (multipart/form-data)
- `DELETE /api/admin/happenings/:id` - Delete happening by ID

### Admin
- `POST /api/admin/login` - Admin login
- `POST /api/admin/logout` - Admin logout
- `GET /api/admin/me` - Get current admin user

## File Upload Structure
```
static/
  uploads/
    events/
      20260214_120744_djnight.jpeg
      [timestamp]_[filename]
    happenings/
      20260214_130530_mou1.jpeg
      [timestamp]_[filename]
```

## How It Works

### Adding Content
1. Admin logs in to dashboard
2. Clicks "Add Event" or "Add Happening" button
3. Fills out form with title, description, date (events only), and image
4. Submits form
5. Backend saves image with unique timestamp filename
6. Database record created with image path
7. Admin redirected to dashboard
8. New content appears on main website immediately

### Deleting Content
1. Admin views content in dashboard
2. Clicks "Delete" button on any card
3. Confirms deletion in popup
4. Backend deletes database record and image file
5. Dashboard refreshes automatically
6. Content removed from main website immediately

### Editing Content
1. Admin views content in dashboard
2. Clicks "Edit" button on any card
3. Redirected to edit form with pre-filled data
4. Can modify title, description, date (events), and optionally replace image
5. Submits updated form
6. Backend updates database record and replaces image if new one provided
7. Admin redirected to dashboard
8. Updated content appears on main website immediately

### Viewing Content on Main Website
- **Events Section**: Shows all active events from database
  - Falls back to 4 default events if database is empty
  - Displays in grid with navigation arrows
  - Shows date badge on each card
  
- **Happenings Section**: Shows all active happenings from database
  - Falls back to 3 default happenings if database is empty
  - Auto-rotating carousel (5 seconds)
  - Manual navigation with arrows
  - Responsive: 3 cards on desktop, 2 on tablet, 1 on mobile

## Database Schema

### Admin Table
- id (Primary Key)
- username (Unique)
- password_hash

### Event Table
- id (Primary Key)
- title
- description
- event_date
- image_path
- is_active (Boolean, default: True)
- created_at
- updated_at

### Happening Table
- id (Primary Key)
- title
- description
- image_path
- is_active (Boolean, default: True)
- created_at
- updated_at

## Security Features
- Password hashing using werkzeug
- File upload validation (type and size)
- Unique filenames to prevent overwrites
- CORS configuration for frontend-backend communication
- Session management with Flask-Login

## Future Enhancements (Optional)
- Bulk delete
- Image cropping/resizing
- Rich text editor for descriptions
- Event categories/tags
- Search and filter in dashboard
- Analytics dashboard
- Drag and drop image upload
- Multiple image upload per event/happening
