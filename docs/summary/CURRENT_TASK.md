# COMPLETED TASK SUMMARY: User Profile Function Implementation

## Task Overview

# CURRENT TASK SUMMARY: Member Managment Structure - Backend Implementation

## Task Overview
Build a relationship table between user and members. User can create and edit 

## UserToMember Model

### UserToMember Class
**File**: `backend/app/models/usertomember.py`
**Table**: `usertomember`

The usertomember model represents relationship between user and their family members. User can create/manager new members for his relationshp and decide which member is OK to share. He can invite other user to the relationship. Once other user accepted the invitation, the invited user will estabilish new reltionship with the existing memebers of the group but can only view them. The relationship needs to be auto calculated. 

#### Fields

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | Primary Key, Index | Unique identifier for each relationship |
| `user_id` | Integer | Foreign Key, Not Null | Reference to User |
| `member_id` | Integer | Foreign Key, Not Null | Reference to Member |
| `relationship` | String | Not Null | Enum Relationship between the member and the user (child, spouse, parent, etc) |
| `is_shareable` | Boolean | Default: True | The user can determine if the member (only for the members managed by the user) is good to share with other invited member (who is also a user) |
| `is_manager` | Boolean | Default: True | The user can edit/delete the memeber or not |
| `created_at` | DateTime | Default: now | Record creation timestamp |
| `updated_at` | DateTime | Auto-update | Last modification timestamp |

#### Key Features
- **Member Manager**: If the memeber is created by a user, then the user is the manager of the members
- **User Invite**: If the memeber is invited by a user, then the user is the viewer of the members
- **Invitation accepted**: If another user accepted the invitation, then the user will establish a new relationship with the invited user. The invited user will also establish relationships with all the sharable memebers. (A invitation model maybe needed here.)
- **Calculated Relationship**: The new relationship between the invited user and sharable members are calculated by the existing relationship between them.