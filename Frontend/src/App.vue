<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router";
</script>

<template>
  <!-- <div class="py-2 px-5">
    <div class="text-8xl text-red-700">Wreck It</div>
  </div> -->
  <header>
    <div class="bg-zinc-900">
      <nav>
        <RouterLink to="/" class="nav-link">Users</RouterLink>
        <RouterLink to="/teams" class="nav-link">Teams</RouterLink>
        <RouterLink to="/coupons" class="nav-link">Coupons</RouterLink>
        <RouterLink to="/stats" class="nav-link">Stats</RouterLink>
        <RouterLink to="/scripts" class="nav-link">Scripts</RouterLink>
      </nav>
    </div>
  </header>

  <RouterView />
</template>

<style scoped>
header {
  line-height: 1;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
  display: flex;
  justify-content: center;
}

nav a {
  display: inline-block;
  padding: 0 1rem; /* Apply padding to all links */
  border-left: 1px solid var(--color-border);
  font-size: 50px;
  color: rgb(107 114 128);
}

nav a:first-of-type {
  border: 0;
}

.nav-link.router-link-exact-active {
  color: rgb(52 211 153);
}

.nav-link.router-link-exact-active:hover {
  background-color: transparent;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: 0.2rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }

  main {
    display: flex;
    justify-content: center;
    align-items: center;
  }
}
</style>
