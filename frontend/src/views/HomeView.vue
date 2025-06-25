<template>
    <main class="container-md mx-auto mt-5">
        <input type="text" class="d-block w-100 text-center">
        <table class="table">
            <thead>
                <tr>
                    <th>1</th>
                    <th>2</th>
                    <th>3</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>A</td>
                    <td>Bunch</td>
                    <td>Of</td>
                </tr>
                <tr>
                    <td>Test</td>
                    <td>ing</td>
                    <td>Data</td>
                </tr>
                <tr>
                    <td>Is</td>
                    <td>Here</td>
                    <td>!</td>
                </tr>
            </tbody>
        </table>
    </main>
    
    <router-link 
        to="/admin" 
        class="position-fixed bottom-0 end-0 btn btn-secondary">
        Admin
    </router-link>
</template>