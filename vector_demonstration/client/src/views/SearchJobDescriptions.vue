<template>
  <div class="flex">
    <h1>SEARCH JOB DESCRIPTIONS</h1>
  </div>
</template>

<script>
import { ref } from 'vue'
import  { jobDescriptionApi } from '@/services/jobDescriptions/'

export default {
  name: 'SearchJobDescriptions',
  components: {
  //   InputField,
  },
  setup() {
  //   const store = useStore()
  //   const router = useRouter()
  //   const form = ref(new LoginForm())

    function search() {
    // unwrap form
    // const unwrappedForm = form.value
    // unwrappedForm.validate()
    // if (!unwrappedForm.isValid) return

    jobDescriptionApi.csc
        .search({ query: "This student excels at accounting and data analysis." })
        .then(handleLoginSuccess)
        .catch(handleLoginFailure)
    }

    return {
      // form,
      search,
    }
  },
}
</script>

<style scoped lang="css"></style>
