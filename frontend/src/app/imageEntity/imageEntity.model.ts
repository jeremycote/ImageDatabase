export class ImageEntity {
    constructor(
        public filename: string,
        public path: string,
        public description: string,
        public id?: number,
        public updatedAt?: Date,
        public createdAt?: Date
    ) {}
}