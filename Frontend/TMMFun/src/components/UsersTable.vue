<template>
  <div class="px-4 sm:px-6 lg:px-8">
    <div class="mt-8 flow-root">
      <div class="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
        <div class="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
          <table class="min-w-full divide-y divide-gray-300">
            <thead>
              <tr
                v-for="headerGroup in table.getHeaderGroups()"
                :key="headerGroup.id"
              >
                <th
                  v-for="header in headerGroup.headers"
                  :key="header.id"
                  scope="col"
                  class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900"
                >
                  <FlexRender
                    :render="header.column.columnDef.header"
                    :props="header.getContext()"
                  />
                </th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">
              <tr v-for="row in table.getRowModel().rows" :key="row.id">
                <td
                  v-for="cell in row.getVisibleCells()"
                  :key="cell.id"
                  class="whitespace-nowrap px-3 py-4 text-sm text-gray-500"
                >
                  <FlexRender
                    :render="cell.column.columnDef.cell"
                    :props="cell.getContext()"
                  />
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Make sure this block is also TypeScript
import people from "../mockDataPeople.json";
import { ref } from "vue";
import { useVueTable, getCoreRowModel, FlexRender } from "@tanstack/vue-table";
import { format } from "date-fns";

const data = ref(people);

const columnsPeople = [
  {
    accessorKey: "fullname", // Assuming the ID is the first element
    header: "Full Name",
  },
  {
    accessorKey: "email",
    header: "Email",
  },
  {
    accessorKey: "createdAt",
    header: "Created At",
    cell: (info) => format(new Date(info.getValue()), "MMM d, yyyy"),
  },
  {
    accessorKey: "updatedAt",
    header: "Updated At",
    cell: (info) => format(new Date(info.getValue()), "MMM d, yyyy"),
  },
  {
    accessorKey: "picture",
    header: "Picture",
  },
  {
    accessorKey: "tokenBalance",
    header: "Token Balance",
  },
  {
    accessorKey: "public_user_id",
    header: "Public User ID",
  },
  {
    accessorKey: "creator_user_id", // Name
    header: "Creator User ID",
  },
  {
    accessorKey: "passwordhash",
    header: "Password Hash",
  },
  {
    accessorKey: "signupIP",
    header: "Signup IP",
  },
  {
    accessorKey: "institution",
    header: "Instituiton",
  },
  {
    accessorKey: "bio",
    header: "Bio",
  },
  {
    accessorKey: "id",
    header: "ID",
  },
  {
    accessorKey: "edit",
    header: " ",
  },
];

const table = useVueTable({
  data: data.value,
  columns: columnsPeople,
  getCoreRowModel: getCoreRowModel(),
});
</script>

<script lang="ts">
export default {
  name: "PeopleTable",
};
</script>
