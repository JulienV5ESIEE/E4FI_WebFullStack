<template>
  <div>
    <h1>Login</h1>
    <form @submit.prevent="submitForm">
      <label>
        Password:
        <input type="password" v-model="password">
      </label>
      <button type="submit">Submit</button>
    </form>
  </div>
</template>

<script>
export default {
 name: "LoginPage",
  data() {
    return {
      password: ''
    };
  },
  methods: {
    async submitForm() {
      try {
        const response = await fetch('/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ password: this.password })
        });

        if (response.ok) {
          const data = await response.json();
          localStorage.setItem('token', data.token);
          // Rediriger vers une autre page ici si l'authentification est réussie
        } else {
          console.error('Error:', response);
          alert('Invalid password');
        }
      } catch (error) {
        console.error('Error:', error);
      }
    }
  }
};
</script>
