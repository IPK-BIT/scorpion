import Home from "../routes/Home.svelte";
import Submission from "../routes/Submission.svelte";
import Registration from "../routes/Registration.svelte";
import Administration from "../routes/Administration.svelte";
import Profile from "../routes/Profile.svelte";
import NotFound from "../routes/NotFound.svelte";
import FooterDetails from "../routes/FooterDetails.svelte";

export const routes = {
    "/": Home,
    "/submit": Submission,
    "/register": Registration,
    "/admin": Administration,
    "/profile": Profile,
    '/how-to-cite': FooterDetails,
    '/terms-of-use': FooterDetails,
    '/privacy': FooterDetails,
    '/contact': FooterDetails,
    '/about': FooterDetails,
    "*": NotFound
}