<script setup>
import { ref } from 'vue';

const formData = ref({
  name: '',
  email: '',
  age: null,
});

const handleSubmit = () => {
  // Handle form submission logic here
  console.log('Form submitted:', formData.value);
};
</script>

<template>
  <div class="center-box">
    <div class="form-box">
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="name">Name:</label>
          <input type="text" id="name" v-model="formData.name" required />
        </div>
        <div class="form-group">
          <label for="email">Email:</label>
          <input type="tex" id="email" v-model="formData.email" required />
        </div>
        <div class="form-group">
          <label for="age">Age:</label>
          <input type="text" id="age" v-model="formData.age" required />
        </div>
        <button type="submit">Submit</button>
      </form>
    </div>
  </div>
</template>

<style scoped>
.center-box {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.form-box {
  width: 300px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  background-color: #4caf50;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>