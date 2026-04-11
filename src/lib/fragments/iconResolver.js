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
// Navigation icons
import ShowChartIcon from '@mui/icons-material/ShowChart';
import BarChartIcon from '@mui/icons-material/BarChart';
import PieChartIcon from '@mui/icons-material/PieChart';
import ScatterPlotIcon from '@mui/icons-material/ScatterPlot';
import GridOnIcon from '@mui/icons-material/GridOn';
import TimelineIcon from '@mui/icons-material/Timeline';
import CandlestickChartIcon from '@mui/icons-material/CandlestickChart';
import SpeedIcon from '@mui/icons-material/Speed';
import LayersIcon from '@mui/icons-material/Layers';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import HistoryIcon from '@mui/icons-material/History';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import TuneIcon from '@mui/icons-material/Tune';
import BrushIcon from '@mui/icons-material/Brush';
import HighlightIcon from '@mui/icons-material/Highlight';
import SyncIcon from '@mui/icons-material/Sync';
import ZoomInIcon from '@mui/icons-material/ZoomIn';
import TouchAppIcon from '@mui/icons-material/TouchApp';
import TableChartIcon from '@mui/icons-material/TableChart';
import StackedBarChartIcon from '@mui/icons-material/StackedBarChart';
import PaletteIcon from '@mui/icons-material/Palette';
import RuleIcon from '@mui/icons-material/Rule';
import MouseIcon from '@mui/icons-material/Mouse';
import CheckBoxIcon from '@mui/icons-material/CheckBox';
import UnfoldMoreIcon from '@mui/icons-material/UnfoldMore';
import BlockIcon from '@mui/icons-material/Block';
import DiamondIcon from '@mui/icons-material/Diamond';
import AutoGraphIcon from '@mui/icons-material/AutoGraph';
import ViewListIcon from '@mui/icons-material/ViewList';
import GpsFixedIcon from '@mui/icons-material/GpsFixed';

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
    // Navigation
    ShowChart: ShowChartIcon,
    BarChart: BarChartIcon,
    PieChart: PieChartIcon,
    ScatterPlot: ScatterPlotIcon,
    GridOn: GridOnIcon,
    Timeline: TimelineIcon,
    CandlestickChart: CandlestickChartIcon,
    Speed: SpeedIcon,
    Layers: LayersIcon,
    TrendingUp: TrendingUpIcon,
    History: HistoryIcon,
    PlayArrow: PlayArrowIcon,
    Tune: TuneIcon,
    Brush: BrushIcon,
    Highlight: HighlightIcon,
    Sync: SyncIcon,
    ZoomIn: ZoomInIcon,
    TouchApp: TouchAppIcon,
    TableChart: TableChartIcon,
    StackedBarChart: StackedBarChartIcon,
    Palette: PaletteIcon,
    Rule: RuleIcon,
    Mouse: MouseIcon,
    CheckBox: CheckBoxIcon,
    UnfoldMore: UnfoldMoreIcon,
    Block: BlockIcon,
    Diamond: DiamondIcon,
    AutoGraph: AutoGraphIcon,
    ViewList: ViewListIcon,
    GpsFixed: GpsFixedIcon,
};

/**
 * Resolve an icon name string to a MUI icon component.
 * Returns undefined if the name is not recognized.
 */
export const resolveIcon = (name) => {
    if (!name) return undefined;
    return ICON_MAP[name] || undefined;
};
