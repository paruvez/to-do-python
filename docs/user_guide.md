
## 7. User Guide (docs/user_guide.md)

```markdown
# TodoMaster Pro - User Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Managing Tasks](#managing-tasks)
3. [Categories & Tags](#categories--tags)
4. [Filters & Search](#filters--search)
5. [Statistics](#statistics)
6. [Exporting Data](#exporting-data)
7. [Keyboard Shortcuts](#keyboard-shortcuts)
8. [Troubleshooting](#troubleshooting)

## Getting Started

### First Launch
When you first launch TodoMaster Pro, you'll see:
- Empty task list
- Pre-defined categories
- Statistics dashboard
- Quick access toolbar

### Adding Your First Task
1. Click the **+ Add Task** button
2. Enter a task title (required)
3. Add description (optional)
4. Set priority (High/Medium/Low)
5. Choose due date (optional)
6. Select category
7. Click **Save**

### Understanding the Interface

**Header Section**
- App logo and title
- Quick stats (Total/Pending/Completed)
- Search box

**Sidebar**
- Quick filters (All/Pending/Completed/etc.)
- Category list
- Add category button

**Main Content**
- Task list table
- Action buttons (Complete/Edit/Delete)
- Statistics dashboard

**Status Bar**
- App information
- Current status
- Time display

## Managing Tasks

### Creating Tasks
You can create tasks in several ways:
1. **Toolbar button**: Click + Add Task
2. **Keyboard shortcut**: Ctrl + N
3. **Right-click** in empty area of task list

### Editing Tasks
To edit a task:
1. **Double-click** the task in the list
2. Or select task and click **✏️ Edit**
3. Make changes in the dialog
4. Click **Save**

### Completing Tasks
Mark a task as completed:
1. Select the task
2. Click **✅ Complete** button
3. Or use context menu option

Completed tasks appear grayed out in the list.

### Deleting Tasks
Delete unwanted tasks:
1. Select the task
2. Click **🗑️ Delete** button
3. Confirm deletion in dialog

**Warning**: Deleted tasks cannot be recovered!

### Task Properties
Each task has:
- **Title**: Main task description (required)
- **Description**: Detailed notes (optional)
- **Priority**: High/Medium/Low (affects color coding)
- **Due Date**: Deadline (optional)
- **Category**: Organization group
- **Status**: Pending/Completed
- **Created At**: Auto-generated timestamp
- **Completed At**: Auto-filled when completed

## Categories & Tags

### Default Categories
The app comes with these categories:
- **General**: Default category
- **Work**: Professional tasks
- **Personal**: Personal matters
- **Shopping**: Purchase items
- **Health**: Fitness and wellness
- **Education**: Learning goals
- **Finance**: Money management
- **Travel**: Trip planning

### Creating Custom Categories
1. Click **+ Add Category** in sidebar
2. Enter category name
3. Choose a color
4. Click **Add**

### Managing Categories
- Categories appear in sidebar
- Click to filter tasks by category
- Colors help visual identification
- Category cannot be deleted if tasks exist

### Color Coding
- Each category has a color
- Color appears as dot next to category name
- Helps quick identification
- Customizable during creation

## Filters & Search

### Quick Filters
Sidebar provides one-click filters:
- **📋 All Tasks**: Show all tasks
- **⏳ Pending**: Incomplete tasks only
- **✅ Completed**: Finished tasks only
- **⚠️ Overdue**: Past due tasks only
- **📅 Today**: Tasks due today only

### Category Filters
- Click any category in sidebar
- Shows tasks only from that category
- Click **All Categories** to clear filter

### Search Functionality
The search box allows you to:
- Search by task title
- Search by description
- Real-time filtering
- Case-insensitive search

**Search Tips**:
- Type to filter instantly
- Clear search box to show all
- Search works with active filters

### Combining Filters
You can combine:
- Category filter + Quick filter
- Category filter + Search
- Quick filter + Search
- All three together

## Statistics

### Dashboard Overview
The statistics dashboard shows:
- **Total Tasks**: Overall count
- **Completed**: Finished tasks
- **Pending**: Incomplete tasks
- **Overdue**: Late tasks
- **Today**: Due today
- **Productivity**: Completion percentage

### Progress Bar
- Visual representation of completion rate
- Updates in real-time
- Color-coded based on percentage
- Shows exact percentage number

### Header Statistics
Quick stats in header show:
- **Total**: All tasks count
- **Pending**: Tasks to complete
- **Completed**: Finished tasks

These update as you work.

### Productivity Insights
- **High productivity**: >75% completion
- **Medium productivity**: 50-75% completion
- **Low productivity**: <50% completion

Tips appear based on your productivity level.

## Exporting Data

### Export Formats
Currently supports:
- **CSV** (Comma Separated Values)
- Compatible with Excel, Google Sheets, etc.

### Export Process
1. Click **📊 Export** button
2. Choose save location
3. Enter filename
4. Click **Save**

### Export Contents
The CSV file includes:
- All task fields
- Proper column headers
- Date formatting
- UTF-8 encoding

### Using Exported Data
You can:
- Open in spreadsheet software
- Create charts and graphs
- Perform data analysis
- Backup your tasks

### Export Frequency
- Export regularly for backups
- Export before major changes
- Export for reporting purposes

## Keyboard Shortcuts

### Global Shortcuts
| Shortcut | Action |
|----------|---------|
| `F5` | Refresh task list |
| `Ctrl + N` | Add new task |
| `Ctrl + F` | Focus search box |
| `Ctrl + S` | Export tasks |
| `Delete` | Delete selected task |
| `Esc` | Close dialog/cancel |

### Navigation Shortcuts
| Shortcut | Action |
|----------|---------|
| `↑/↓` | Navigate task list |
| `Enter` | Edit selected task |
| `Space` | Complete selected task |
| `Tab` | Navigate between fields |

### Dialog Shortcuts
| Shortcut | Action |
|----------|---------|
| `Ctrl + Enter` | Save/Save & Close |
| `Esc` | Cancel/Close |
| `Tab` | Next field |
| `Shift + Tab` | Previous field |

### Search Shortcuts
| Shortcut | Action |
|----------|---------|
| `Ctrl + F` | Focus search |
| `Esc` | Clear search |
| `Enter` | Execute search |

## Troubleshooting

### Common Issues

**1. Application won't start**
- Check Python installation
- Verify Tkinter is installed
- Check error messages in terminal

**2. Database errors**
- Close and restart application
- Check file permissions
- Backup and reset database

**3. Missing features**
- Update to latest version
- Check configuration
- Reinstall application

**4. Slow performance**
- Reduce number of tasks
- Clear old completed tasks
- Restart application

### Error Messages

**"Database locked"**
- Another instance might be running
- Close all instances and restart
- Check for background processes

**"Import error"**
- Missing Python packages
- Run: `pip install -r requirements.txt`
- Check Python version

**"Tkinter not found"**
- Install Tkinter for your system
- Reinstall Python with Tkinter support

### Data Recovery

**Backup Files**
- Automatic backups in `backups/` folder
- Manual exports in `exports/` folder
- Database file: `todo_app.db`

**Restoring Data**
1. Close application
2. Replace `todo_app.db` with backup
3. Restart application

**Export/Import**
1. Export current data
2. Clear/reset application
3. Manually re-import if needed

### Getting Help

**Documentation**
- Check this user guide
- Read README.md file
- View source code comments

**Support Channels**
- GitHub Issues
- Email support
- Social media: @paruuvez

**Reporting Bugs**
1. Describe the issue
2. Include steps to reproduce
3. Add screenshots if possible
4. Share system information

---

*For additional help, contact: Parvez Zamadar (@paruuvez)*
