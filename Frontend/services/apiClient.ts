import useAxios from "./apiService";

export const getUsers = () => {
  return useAxios.get("/users");
};

export const editUser = (id, data) => {
  console.log("Editing user with ID:", id);
  console.log("Data:", data);

  return useAxios.put(`/user/${id}`, data);
};

export const deleteUsers = (userIDs) => {
  return useAxios.delete(`/users/delete`, { data: { userIDs: userIDs } });
};
