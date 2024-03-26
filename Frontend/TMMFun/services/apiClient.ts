import useAxios from "./apiService";

export const getUsers = () => {
  return useAxios.get("/users");
};
