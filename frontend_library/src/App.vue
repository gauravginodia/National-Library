<template>
  

  <div>
    <div>
      <router-view />
    </div>
  </div>
  
</template>
<script>
export default {
  name: 'App',  
  components: {
  },
  computed: {
    checkPage() {
      if(this.$route.name === 'App')
      {
        return 1;

      }
      else
        {
          return 0;
        }

    },
  },
};
</script>

<style>

/* Add your scoped styles here */
</style>
