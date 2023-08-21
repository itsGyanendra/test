<template>
  <div>
    <div>
      <UserVariableCreationForm
        ref="UserVariableCreationForm"
        :challenge_id="challenge_id"
        :uservariables="uservariables"
        @refreshUserVariables="refreshUserVariables"
      />
    </div>

    <div>
      <UserVariableEditForm
        ref="UserVariableEditForm"
        :challenge_id="challenge_id"
        :uservariable_id="editing_uservariable_id"
        :uservariables="uservariables"
        @refreshUserVariables="refreshUserVariables"
      />
    </div>

    <table class="table table-striped">
      <thead>
        <tr>
          <td class="text-center"><b>User Email</b></td>
          <td class="text-center"><b>Variable Name</b></td>
          <td class="text-center"><b>Variable Value</b></td>
          <td class="text-center"><b>Settings</b></td>
        </tr>
      </thead>
      <tbody>
        <tr v-for="uservariable in uservariables" :key="uservariable.id">
          <td class="text-center">{{ uservariable.user_email }}</td>
          <td class="text-center">{{ uservariable.variable_name }}</td>
          <td class="text-center">{{ uservariable.variable_value }}</td>
          <td class="text-center">
            <i
              role="button"
              class="btn-fa fas fa-edit"
              @click="editUserVariable(uservariable.id)"
            ></i>
            <i
              role="button"
              class="btn-fa fas fa-times"
              @click="deleteUserVariable(uservariable.id)"
            ></i>
          </td>
        </tr>
      </tbody>
    </table>
    <div class="col-md-12">
      <button class="btn btn-success float-right" @click="addUserVariable">
        Create User Variable
      </button>
    </div>
  </div>
</template>

<script>
import { ezQuery } from "core/ezq";
import CTFd from "core/CTFd";
import UserVariableCreationForm from "./UserVariableCreationForm.vue";
import UserVariableEditForm from "./UserVariableEditForm.vue";

export default {
  components: {
    UserVariableCreationForm,
    UserVariableEditForm
  },
  props: {
    challenge_id: Number
  },
  data: function() {
    return {
      uservariables: [],
      editing_uservariable_id: null
    };
  },
  methods: {
    loadUserVariables: function() {
      CTFd.fetch(`/api/v1/challenges/${this.$props.challenge_id}/uservariables`, {
        method: "GET",
        credentials: "same-origin",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json"
        }
      })
        .then(response => {
          return response.json();
        })
        .then(response => {
          if (response.success) {
            this.uservariables = response.data;
          }
        });
    },
    addUserVariable: function() {
      let modal = this.$refs.UserVariableCreationForm.$el;
      $(modal).modal();
    },
    editUserVariable: function(uservariableId) {
      this.editing_uservariable_id = uservariableId;
      let modal = this.$refs.UserVariableEditForm.$el;
      $(modal).modal();
    },
    refreshUserVariables: function(caller) {
      this.loadUserVariables();
      let modal;
      switch (caller) {
        case "UserVariableCreationForm":
          modal = this.$refs.UserVariableCreationForm.$el;
          console.log(modal);
          $(modal).modal("hide");
          break;
        case "UserVariableEditForm":
          modal = this.$refs.UserVariableEditForm.$el;
          $(modal).modal("hide");
          break;
        default:
          break;
      }
    },
    deleteUserVariable: function(uservariableId) {
      ezQuery({
        title: "Delete User Variable",
        body: "Are you sure you want to delete this user variable?",
        success: () => {
          CTFd.fetch(`/api/v1/uservariables/${uservariableId}`, {
            method: "DELETE"
          })
            .then(response => {
              return response.json();
            })
            .then(data => {
              if (data.success) {
                this.loadUserVariables();
              }
            });
        }
      });
    }
  },
  created() {
    this.loadUserVariables();
  }
};
</script>

<style scoped></style>
