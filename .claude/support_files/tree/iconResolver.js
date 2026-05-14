/**
 * iconResolver.js — Maps icon name strings to MUI icon components.
 *
 * Dash can't pass React components as props, so we accept string names
 * like "ExpandMore" and resolve them to the actual MUI icon.
 *
 * Claude Code: Expand this map as needed. Consider lazy-loading icons
 * or using @mui/icons-material with dynamic import if bundle size is a concern.
 */
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import FolderIcon from '@mui/icons-material/Folder';
import FolderOpenIcon from '@mui/icons-material/FolderOpen';
import InsertDriveFileIcon from '@mui/icons-material/InsertDriveFile';
import RemoveIcon from '@mui/icons-material/Remove';
import AddIcon from '@mui/icons-material/Add';
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';
import ArrowRightIcon from '@mui/icons-material/ArrowRight';

const ICON_MAP = {
    ExpandMore: ExpandMoreIcon,
    ChevronRight: ChevronRightIcon,
    Folder: FolderIcon,
    FolderOpen: FolderOpenIcon,
    InsertDriveFile: InsertDriveFileIcon,
    Remove: RemoveIcon,
    Add: AddIcon,
    ArrowDropDown: ArrowDropDownIcon,
    ArrowRight: ArrowRightIcon,
};

/**
 * Resolve an icon name string to a MUI icon component.
 * Returns undefined if the name is not recognized.
 */
export const resolveIcon = (name) => {
    if (!name) return undefined;
    return ICON_MAP[name] || undefined;
};
