import { createRouter, createWebHistory } from 'vue-router';

// Import components for routes
import UserAuthentication from "../views/UserAuthentication.vue";
import LibrarianAuthentication from "../views/LibrarianAuthentication.vue";
import RegisterUser from "../views/RegisterUser.vue";
import UserDashboard from "../views/User/UserDashboard.vue";
import SectionManagement from "../views/Librarian/SectionManagement.vue";
import BooksbySection from "../views/Librarian/BooksbySection.vue";
import IssuedBooks from "../views/User/IssuedBooks.vue";
import RequestedReading from "../views/Librarian/RequestedReading.vue";
import AssignedBooks from "../views/Librarian/AssignedBooks.vue";
import StatusBooks from '../views/Librarian/StatusBooks.vue';
import UserHistory from '../views/User/UserHistory.vue';
import BookPage from '../views/User/BookPage.vue';
import StatsDashboard from '@/views/Librarian/StatsDashboard.vue';
const isAuthenticated = () => {
  return !!localStorage.getItem('accessToken');
};

const isUser = () => {
  return localStorage.getItem('userType') === 'user';
};

const isLibrarian = () => {
  return localStorage.getItem('userType') === 'librarian';
};

const requireAuth = (to, from, next) => {
  if (!isAuthenticated()) {
    next('/');
  } else {
    next();
  }
};

const requireUser = (to, from, next) => {
  if (!isUser()) {
    next('/');
  } else {
    next();
  }
};

const requireLibrarian = (to, from, next) => {
  if (!isLibrarian()) {
    next('/');
  } else {
    next();
  }
};

// Routes configuration
const routes = [
  // Public routes
  { path: '/', component: UserAuthentication, meta: { title: "Home" } },
  { path: '/librarian/login', component: LibrarianAuthentication, meta: { title: "Librarian Login" } },
  { path: '/RegisterUser', component: RegisterUser, meta: { title: "User Signup" } },
  // User routes
  {
    path: '/user/dashboard',
    component: UserDashboard,
    meta: { title: "Dashboard" },
    beforeEnter: [requireAuth, requireUser]
  },
  { path: '/user/dashboard/history', name: 'UserHistory', component: UserHistory ,meta: { title: "User History" },beforeEnter: [requireAuth, requireUser]},
  { path: '/user/dashboard/issuedbooks', name: 'IssuedBooks', component: IssuedBooks ,meta: { title: "User Books" },beforeEnter: [requireAuth, requireUser]},
  { path: '/user/dashboard/books/:id', name: 'BookPage', component: BookPage ,meta: { title: "Book Page" },beforeEnter: [requireAuth, requireUser]},

  { path: '/librarian/dashboard',name: 'StatsDashboard',component: StatsDashboard,meta: { title: "Dashboard" },beforeEnter: [requireAuth, requireLibrarian]},
  { path: '/librarian/dashboard/sections', name: 'SectionManagement', component: SectionManagement, meta: { title: "Book" } },
  { path: '/librarian/dashboard/section/:id/:name', name: 'BooksbySection', component: BooksbySection, props: true, meta: { title: "Book" } },
  { path: '/librarian/dashboard/requestedbooks', name: 'RequestedReading', component: RequestedReading, meta: { title: "Requested Books" } },
  { path: '/librarian/dashboard/assignedbooks', name: 'AssignedBooks', component: AssignedBooks, meta: { title: "Allocated Books" } },
  { path: '/librarian/dashboard/bookstatus', name: 'StatusBooks', component: StatusBooks, meta: { title: "Available Books" } },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

router.beforeEach((to, from, next) => {
  document.title = to.meta.title || 'Library Management System';
  next();
});

export default router;
