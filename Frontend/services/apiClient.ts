import useAxios from "./apiService";

export const getUsers = () => {
  return useAxios.get("/users");
};

export const getTeams = () => {
  return useAxios.get("/teams");
};

export const getCoupons = () => {
  return useAxios.get("/coupons");
};

export const getUserStats = () => {
  return useAxios.get("/accounts/creation-stats");
};

export const editUser = (id, data) => {
  console.log("Editing user with ID:", id);
  console.log("Data:", data);

  return useAxios.put(`/user/${id}`, data);
};

export const editTeam = (id: String, data: Object) => {
  console.log("Editing team with ID:", id);
  console.log("Data:", data);

  return useAxios.put(`/team/${id}`, data);
};

export const deleteUsers = (userIDs) => {
  return useAxios.delete(`/users/delete`, { data: { userIDs: userIDs } });
};

export const updateUsersPictureURL = async (userIDs, newPictureURL) => {
  try {
    await useAxios.put("/users/update-picture-url", { userIDs, newPictureURL });
  } catch (error) {
    throw new Error("Error updating picture URLs:", error);
  }
};

export const updateUsersCreatedAt = async (userIDs) => {
  try {
    await useAxios.put("/users/update-created-at", { userIDs });
  } catch (error) {
    console.error(error);
  }
};

export const updateTeamsPictureURL = async (teamIDs, newPictureURL) => {
  try {
    await useAxios.put("/teams/update-picture-url", { teamIDs, newPictureURL });
  } catch (error) {
    throw new Error("Error updating picture URLs:", error);
  }
};
