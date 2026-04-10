/**
 * iconResolver.js — Maps icon name strings to MUI icon components.
 *
 * Dash can't pass React components as props, so we accept string names
 * like "ExpandMore" and resolve them to the actual MUI icon.
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
import AccountTreeIcon from '@mui/icons-material/AccountTree';
import DescriptionIcon from '@mui/icons-material/Description';
import CodeIcon from '@mui/icons-material/Code';
import ImageIcon from '@mui/icons-material/Image';
import SettingsIcon from '@mui/icons-material/Settings';
import HomeIcon from '@mui/icons-material/Home';
import StarIcon from '@mui/icons-material/Star';
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Edit';
import VisibilityIcon from '@mui/icons-material/Visibility';
import LockIcon from '@mui/icons-material/Lock';

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
    AccountTree: AccountTreeIcon,
    Description: DescriptionIcon,
    Code: CodeIcon,
    Image: ImageIcon,
    Settings: SettingsIcon,
    Home: HomeIcon,
    Star: StarIcon,
    Delete: DeleteIcon,
    Edit: EditIcon,
    Visibility: VisibilityIcon,
    Lock: LockIcon,
};

/**
 * Resolve an icon name string to a MUI icon component.
 * Returns undefined if the name is not recognized.
 */
export const resolveIcon = (name) => {
    if (!name) return undefined;
    return ICON_MAP[name] || undefined;
};
